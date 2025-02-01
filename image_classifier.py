import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from flask import Flask, request, render_template
import os

app = Flask(__name__)

# Load a pre-trained model (e.g., MobileNetV2)
model = tf.keras.applications.MobileNetV2(weights="imagenet")

# Define allowed file types
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

# Function to check allowed file type
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Function to preprocess image
def preprocess_image(img_path):
    img = image.load_img(img_path, target_size=(224, 224))  # Resize to model input size
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    return img_array

# Route for homepage
@app.route("/", methods=["GET", "POST"])
def upload_file():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file uploaded"
        
        file = request.files["file"]
        if file.filename == "" or not allowed_file(file.filename):
            return "Invalid file type. Upload a JPG or PNG image."
        
        file_path = os.path.join("uploads", file.filename)
        file.save(file_path)

        # Process image and make prediction
        img_array = preprocess_image(file_path)
        preds = model.predict(img_array)
        decoded_preds = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=3)[0]

        # Format results
        result = {entry[1]: round(entry[2] * 100, 2) for entry in decoded_preds}
        return render_template("result.html", result=result, image=file.filename)

    return render_template("upload.html")

if __name__ == "__main__":
    os.makedirs("uploads", exist_ok=True)
    app.run(debug=True)
