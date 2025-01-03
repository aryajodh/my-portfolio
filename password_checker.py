import re
import tkinter as tk
from tkinter import messagebox

def check_password_strength(password):
    strength = 0
    feedback = []

    # Check length
    if len(password) >= 8:
        strength += 1
    else:
        feedback.append("Password should be at least 8 characters long.")

    # Check for uppercase letters
    if re.search(r"[A-Z]", password):
        strength += 1
    else:
        feedback.append("Include at least one uppercase letter.")

    # Check for lowercase letters
    if re.search(r"[a-z]", password):
        strength += 1
    else:
        feedback.append("Include at least one lowercase letter.")

    # Check for numbers
    if re.search(r"[0-9]", password):
        strength += 1
    else:
        feedback.append("Include at least one digit.")

    # Check for special characters
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):  # Matches common special characters
        strength += 1
    else:
        feedback.append("Include at least one special character.")

    # Clamp strength to valid indices of levels
    levels = ["Very Weak", "Weak", "Moderate", "Strong", "Very Strong"]
    strength = min(strength, len(levels) - 1)
    strength_level = levels[strength]

    return strength, strength_level, feedback


def main_loop():
    print("Welcome to the Password Strength Checker!")

    while True:
        password = input("\nEnter a password to check its strength (or type 'exit' to quit): ")
        if password.lower() == 'exit':
            print("Goodbye!")
            break

        strength, strength_level, feedback = check_password_strength(password)
        print(f"\nPassword Strength: {strength_level} ({strength}/5)")

        if feedback:
            print("\nSuggestions to improve your password:")
            for suggestion in feedback:
                print(f"- {suggestion}")

# GUI Application using Tkinter
def evaluate_password():
    password = password_entry.get()
    if not password:
        messagebox.showwarning("Input Error", "Please enter a password.")
        return

    strength, strength_level, feedback = check_password_strength(password)
    result_text.set(f"Password Strength: {strength_level} ({strength}/5)")

    suggestions_text.set("\n".join(feedback) if feedback else "Great password! No suggestions.")

def create_gui():
    global password_entry, result_text, suggestions_text

    root = tk.Tk()
    root.title("Password Strength Checker")

    # Input Label
    tk.Label(root, text="Enter Password:").pack(pady=5)

    # Input Field
    password_entry = tk.Entry(root, show="*", width=30)
    password_entry.pack(pady=5)

    # Check Button
    tk.Button(root, text="Check Strength", command=evaluate_password).pack(pady=10)

    # Result Label
    result_text = tk.StringVar()
    tk.Label(root, textvariable=result_text, fg="blue").pack(pady=5)

    # Suggestions Label
    suggestions_text = tk.StringVar()
    tk.Label(root, textvariable=suggestions_text, fg="green", wraplength=400, justify="left").pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    mode = input("Choose mode: (1) CLI (2) GUI: ").strip()

    if mode == "1":
        main_loop()
    elif mode == "2":
        create_gui()
    else:
        print("Invalid option. Please choose 1 for CLI or 2 for GUI.")
