import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import os
import schedule
import time
from datetime import datetime
import threading
import tkinter as tk
from tkinter import messagebox

# Email configuration
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
report_schedule_time = "09:00"  # Default schedule time


# Generate the report
def generate_report():
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = f"Daily report generated on {current_time}\n\nHere is the content of the report."
    return report


# Function to send email
def send_email(smtp_info, report_content, attachment_path):
    msg = MIMEMultipart()
    msg['From'] = smtp_info['sender_email']
    msg['To'] = smtp_info['recipient_email']
    msg['Subject'] = "Daily Report"

    msg.attach(MIMEText(report_content, 'plain'))

    # Attach file
    if attachment_path:
        try:
            attachment_name = os.path.basename(attachment_path)
            with open(attachment_path, "rb") as attachment:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition",
                    f"attachment; filename= {attachment_name}",
                )
                msg.attach(part)
        except Exception as e:
            print(f"Failed to attach file: {e}")

    # Send email
    try:
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(smtp_info['sender_email'], smtp_info['sender_password'])
        server.send_message(msg)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print(f"Failed to send email: {e}")


# Function to generate and send report daily
def send_daily_report(smtp_info):
    report_content = generate_report()
    attachment_path = entry_attachment.get()  # Get the attachment path from the GUI
    send_email(smtp_info, report_content, attachment_path)


# Schedule the task to run every day at a specified time
def schedule_report(smtp_info):
    schedule.every().day.at(report_schedule_time).do(send_daily_report, smtp_info)
    while True:
        schedule.run_pending()
        time.sleep(60)


# Start scheduling in a separate thread
def start_scheduler(smtp_info):
    scheduler_thread = threading.Thread(target=schedule_report, args=(smtp_info,))
    scheduler_thread.daemon = True
    scheduler_thread.start()


# Function to start the process when the button is clicked
def start_process():
    smtp_info = {
        'sender_email': entry_sender_email.get(),
        'sender_password': entry_sender_password.get(),
        'recipient_email': entry_recipient_email.get()
    }

    if not all(smtp_info.values()) or not entry_attachment.get():
        messagebox.showwarning("Input Error", "Please fill in all fields.")
        return

    start_scheduler(smtp_info)
    messagebox.showinfo("Success", "Scheduler started!")


# Setting up the GUI
root = tk.Tk()
root.title("Daily Email Report Scheduler")

# Input fields for email configuration
tk.Label(root, text="Sender Email:").grid(row=0, column=0, padx=10, pady=10)
entry_sender_email = tk.Entry(root, width=30)
entry_sender_email.grid(row=0, column=1)

tk.Label(root, text="Sender Password:").grid(row=1, column=0, padx=10, pady=10)
entry_sender_password = tk.Entry(root, show='*', width=30)
entry_sender_password.grid(row=1, column=1)

tk.Label(root, text="Recipient Email:").grid(row=2, column=0, padx=10, pady=10)
entry_recipient_email = tk.Entry(root, width=30)
entry_recipient_email.grid(row=2, column=1)

tk.Label(root, text="Attachment Path:").grid(row=3, column=0, padx=10, pady=10)
entry_attachment = tk.Entry(root, width=30)
entry_attachment.grid(row=3, column=1)

# Button to start the email scheduler
btn_start = tk.Button(root, text="Start Scheduler", command=start_process)
btn_start.grid(row=4, column=0, columnspan=2, pady=10)

# Start the GUI main loop
root.mainloop()
