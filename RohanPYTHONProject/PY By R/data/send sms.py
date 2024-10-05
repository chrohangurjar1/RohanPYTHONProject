import tkinter as tk
from tkinter import messagebox, font
from twilio.rest import Client

# Twilio configuration
account_sid = 'xxxxxxx'  # Replace with your Account SID
auth_token = 'xxxxxxx'      # Replace with your Auth Token
twilio_phone_number = '+91 xxxxxx'  # Replace with your Twilio phone number

# Create Twilio client
client = Client(account_sid, auth_token)

# Function to send SMS
def send_sms():
    to_phone_number = to_entry.get()
    message = message_entry.get("1.0", tk.END).strip()  # Get message from the text area

    if not to_phone_number or not message:
        messagebox.showwarning("Input Error", "Please enter both phone number and message.")
        return

    try:
        # Send SMS
        message = client.messages.create(
            body=message,
            from_=twilio_phone_number,
            to=to_phone_number
        )
        messagebox.showinfo("Success", f"Message sent successfully! Message SID: {message.sid}")
        clear_inputs()

    except Exception as e:
        messagebox.showerror("Error", f"Failed to send message: {e}")

# Function to clear input fields
def clear_inputs():
    to_entry.delete(0, tk.END)  # Clear the phone number entry
    message_entry.delete("1.0", tk.END)  # Clear the message area

# Function to exit the application
def exit_app():
    root.destroy()

# Create the main window
root = tk.Tk()
root.title("SMS Sender")
root.geometry("400x400")
root.configure(bg="#f0f0f0")  # Light background color

# Create a custom font
custom_font = font.Font(family="Helvetica", size=12)

# Create and place the labels and entries
tk.Label(root, text="Recipient Phone Number (+Country Code)", bg="#f0f0f0", font=custom_font).pack(pady=10)
to_entry = tk.Entry(root, width=30, font=custom_font)
to_entry.pack(pady=5)

tk.Label(root, text="Message", bg="#f0f0f0", font=custom_font).pack(pady=10)
message_entry = tk.Text(root, height=10, width=30, font=custom_font)
message_entry.pack(pady=5)

# Create buttons frame for better layout
buttons_frame = tk.Frame(root, bg="#f0f0f0")
buttons_frame.pack(pady=20)

# Create the buttons
send_button = tk.Button(buttons_frame, text="Send SMS", command=send_sms, bg="#4CAF50", fg="white", font=custom_font, width=10)
send_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(buttons_frame, text="Clear", command=clear_inputs, bg="#2196F3", fg="white", font=custom_font, width=10)
clear_button.pack(side=tk.LEFT, padx=5)

exit_button = tk.Button(buttons_frame, text="Exit", command=exit_app, bg="#f44336", fg="white", font=custom_font, width=10)
exit_button.pack(side=tk.LEFT, padx=5)

# Run the application
root.mainloop()
