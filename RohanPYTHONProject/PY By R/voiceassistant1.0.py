import datetime
import webbrowser
from tkinter import *

import pyttsx3
import speech_recognition as sr
import wikipedia
from PIL import Image, ImageTk

# Initialize the recognizer and speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()


# Function to make the assistant speak
def speak(text):
    engine.say(text)
    engine.runAndWait()


# Function to greet the user
def greet_user():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning! Major")
    elif 12 <= hour < 18:
        speak("Good Afternoon! Major")
    else:
        speak("Good Evening! Major")
    speak("hello major . How can I help you today?")


# Function to take microphone input from the user
def take_command():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            query = recognizer.recognize_google(audio, language='en-in')
            return query.lower()
        except Exception as e:
            return "Yeah"


# Function to handle the assistant's logic
def run_assistant():
    query = take_command()
    result_text.set(f"You said: {query}")

    if 'wikipedia' in query:
        speak("Searching Wikipedia...")
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        result_text.set(f"According to Wikipedia: {results}")
        speak(results)

    elif 'open youtube' in query:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
        result_text.set("Opened YouTube")

    elif 'open google' in query:
        speak("Opening Google")
        webbrowser.open("https://www.google.com")
        result_text.set("Opened Google")

    elif 'time' in query:
        str_time = datetime.datetime.now().strftime("%H:%M:%S")
        result_text.set(f"The time is {str_time}")
        speak(f"The time is {str_time}")

    elif 'exit' in query:
        speak("Goodbye!")
        window.destroy()

    else:
        result_text.set("Sorry, I didn't understand that.")
        speak("Sorry, I didn't understand that.")


# GUI Setup with Tkinter
def start_listening():
    result_text.set("Listening...")
    run_assistant()


# Attractive interface starts here
window = Tk()
window.title("Voice Assistant")
window.geometry("600x400")
window.configure(bg="#282A36")  # Dark theme

# Adding custom fonts and colors
label = Label(window, text="Voice Assistant", font=("Helvetica", 24, "bold"), bg="#282A36", fg="#50FA7B")
label.pack(pady=20)

# Display box for results
result_text = StringVar()
result_label = Label(window, textvariable=result_text, wraplength=500, font=("Arial", 14), bg="#282A36", fg="#F8F8F2")
result_label.pack(pady=10)


# Start listening button with custom styles
def on_enter(e):
    listen_button['background'] = '#6272A4'


def on_leave(e):
    listen_button['background'] = '#44475A'


listen_button = Button(window, text="Start Listening", font=("Helvetica", 16, "bold"), bg="#44475A", fg="#F8F8F2", bd=0,
                       padx=20, pady=10, command=start_listening)
listen_button.pack(pady=20)

# Bind hover effects to buttons
listen_button.bind("<Enter>", on_enter)
listen_button.bind("<Leave>", on_leave)

# Add background image
bg_image = Image.open("soldier.jpg")  # Use any background image
bg_image = bg_image.resize((600, 400), Image.LANCZOS)
bg_photo = ImageTk.PhotoImage(bg_image)

bg_label = Label(window, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Bring text and button to front after placing background
label.lift()
result_label.lift()
listen_button.lift()

# Greet the user initially
greet_user()

# Run the application
window.mainloop()
