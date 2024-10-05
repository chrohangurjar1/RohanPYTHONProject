import tkinter as tk
from tkinter import messagebox

# Function to update the display when a button is pressed
def button_click(value):
    current_text = display_var.get()
    display_var.set(current_text + value)

# Function to clear the display
def clear_display():
    display_var.set("")

# Function to calculate the expression
def calculate():
    try:
        result = eval(display_var.get())
        display_var.set(result)
    except Exception as e:
        messagebox.showerror("Error", "Invalid Input")

# Main GUI window
window = tk.Tk()
window.title("Simple Calculator")
window.geometry("400x600")

# StringVar to store the display value
display_var = tk.StringVar()

# Display Entry (where numbers and results appear)
display = tk.Entry(window, textvariable=display_var, font=("Arial", 24), bd=10, insertwidth=2, width=14, borderwidth=4)
display.grid(row=0, column=0, columnspan=4)

# Button layout for the calculator
buttons = [
    ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
    ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
    ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
    ('C', 4, 0), ('0', 4, 1), ('=', 4, 2), ('+', 4, 3)
]

# Add buttons to the GUI
for (text, row, col) in buttons:
    if text == "=":
        button = tk.Button(window, text=text, padx=40, pady=20, font=("Arial", 18),
                           command=calculate, bg="lightgreen")
    elif text == "C":
        button = tk.Button(window, text=text, padx=40, pady=20, font=("Arial", 18),
                           command=clear_display, bg="lightcoral")
    else:
        button = tk.Button(window, text=text, padx=40, pady=20, font=("Arial", 18),
                           command=lambda t=text: button_click(t))

    button.grid(row=row, column=col)

# Start the GUI loop
window.mainloop()
