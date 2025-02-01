import os
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import numpy as np
from flask import Flask, request, render_template, jsonify
from PIL import Image
import io

# Force TensorFlow to use CPU (Render does not support GPU)
os.environ["CUDA_VISIBLE_DEVICES"] = "-1"

app = Flask(__name__)

# Load MobileNetV2 model at startup
MODEL = tf.keras.applications.MobileNetV2(weights="imagenet")

# Allowed file types
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}

def allowed_file(filename):
    """Check if the uploaded file has a valid image extension."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(img):
    """Preprocess the image for MobileNetV2."""
    img = img.resize((224, 224))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = tf.keras.applications.mobilenet_v2.preprocess_input(img_array)
    return img_array

@app.route("/", methods=["GET"])
def home():
    """Render the upload form."""
    return render_template("upload.html")

@app.route("/predict", methods=["POST"])
def predict():
    """Handle image upload, process it, and return predictions."""
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    if file.filename == "" or not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Upload a JPG or PNG image."}), 400

    try:
        img = Image.open(io.BytesIO(file.read()))  # Read image in-memory
        processed_img = preprocess_image(img)

        # Make prediction
        preds = MODEL.predict(processed_img)
        decoded_preds = tf.keras.applications.mobilenet_v2.decode_predictions(preds, top=3)[0]

        # Format results as {label: confidence}
        result = {entry[1]: round(entry[2] * 100, 2) for entry in decoded_preds}
        return render_template("result.html", result=result, image=file.filename)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Use Render's assigned port
    app.run(host="0.0.0.0", port=port)
