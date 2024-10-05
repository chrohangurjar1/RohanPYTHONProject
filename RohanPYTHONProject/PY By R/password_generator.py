import tkinter as tk
import random
import string
from tkinter import messagebox

# Function to generate password
def generate_password():
    try:
        length = int(entry_length.get())
        if length < 4:
            messagebox.showerror("Error", "Password length should be at least 4.")
            return
        
        characters = ""
        if var_upper.get():
            characters += string.ascii_uppercase
        if var_lower.get():
            characters += string.ascii_lowercase
        if var_digits.get():
            characters += string.digits
        if var_special.get():
            characters += string.punctuation

        if characters == "":
            messagebox.showerror("Error", "Select at least one option!")
            return

        password = "".join(random.choice(characters) for _ in range(length))
        entry_password.delete(0, tk.END)
        entry_password.insert(0, password)
    except ValueError:
        messagebox.showerror("Error", "Please enter a valid length!")

# Function to copy password to clipboard
def copy_password():
    password = entry_password.get()
    if password:
        root.clipboard_clear()
        root.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard!")
    else:
        messagebox.showerror("Error", "No password to copy!")

# Create the main window
root = tk.Tk()
root.title("Password Generator By Rohan Naagar")
root.geometry("400x400")

# Password length label and input
label_length = tk.Label(root, text="Password Length:", font=("Arial", 12))
label_length.pack(pady=10)

entry_length = tk.Entry(root, width=5, font=("Arial", 12))
entry_length.pack()

# Checkboxes for character types
var_upper = tk.BooleanVar()
var_lower = tk.BooleanVar()
var_digits = tk.BooleanVar()
var_special = tk.BooleanVar()

checkbox_upper = tk.Checkbutton(root, text="Include Uppercase Letters (A-Z)", variable=var_upper, font=("Arial", 10))
checkbox_upper.pack(anchor='w')

checkbox_lower = tk.Checkbutton(root, text="Include Lowercase Letters (a-z)", variable=var_lower, font=("Arial", 10))
checkbox_lower.pack(anchor='w')

checkbox_digits = tk.Checkbutton(root, text="Include Digits (0-9)", variable=var_digits, font=("Arial", 10))
checkbox_digits.pack(anchor='w')

checkbox_special = tk.Checkbutton(root, text="Include Special Characters (!@#$%^&*)", variable=var_special, font=("Arial", 10))
checkbox_special.pack(anchor='w')

# Button to generate the password
btn_generate = tk.Button(root, text="Generate Password", command=generate_password, font=("Arial", 12))
btn_generate.pack(pady=20)

# Entry field to display the generated password
entry_password = tk.Entry(root, width=30, font=("Arial", 14))
entry_password.pack(pady=10)

# Button to copy the password to the clipboard
btn_copy = tk.Button(root, text="Copy to Clipboard", command=copy_password, font=("Arial", 12))
btn_copy.pack(pady=10)

# Start the main event loop
root.mainloop()
