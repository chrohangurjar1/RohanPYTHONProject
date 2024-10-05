import tkinter as tk
from tkinter import scrolledtext
import re

class Chatbot:
    def __init__(self):
        self.responses = [
            (r'hi|hello|hey', "Hello! How can I help you?"),
            (r'how are you\??', "I'm just a program, but thanks for asking!"),
            (r'what is your name\??', "I am a simple chatbot."),
            (r'bye|goodbye', "Goodbye! Have a great day!"),
            (r'what do you do\??', "I chat with users and answer their questions."),
            (r'tell me a joke', "Why did the scarecrow win an award? Because he was outstanding in his field!"),
            (r'what is your favorite color\??', "I don't have feelings, but blue is a nice color!"),
            (r'help', "Sure! What do you need help with?"),
            (r'thank you|thanks', "You're welcome! If you have more questions, feel free to ask."),
            (r'who created you\??', "I was created by a Python programmer as a learning project."),
            (r'what is your favorite food\??', "I don't eat, but I hear pizza is quite popular!"),
            (r'what is your name\??', "I am a chatbot, but you can call me Chatty!"),
            (r'what do you think about (.*)\?', "I think {0} is interesting!"),
            (r'what is the weather like in (.*)\?', "I don't have real-time weather updates, but I hope it's nice in {0}!"),
        ]

    def get_response(self, user_input):
        for pattern, response in self.responses:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                if '{0}' in response:  # Check for dynamic placeholder
                    return response.format(match.group(1))  # Insert dynamic content
                return response
        return "Sorry, I don't understand that."

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chatbot")

        self.chatbot = Chatbot()

        self.chat_area = scrolledtext.ScrolledText(self.root, state='disabled', width=50, height=20)
        self.chat_area.grid(row=0, column=0, columnspan=2)

        self.user_input = tk.Entry(self.root, width=48)
        self.user_input.grid(row=1, column=0)

        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1)

    def send_message(self):
        user_text = self.user_input.get()
        self.chat_area.config(state='normal')
        self.chat_area.insert(tk.END, "You: " + user_text + '\n')
        self.user_input.delete(0, tk.END)

        response = self.chatbot.get_response(user_text)
        self.chat_area.insert(tk.END, "Bot: " + response + '\n')
        self.chat_area.config(state='disabled')
        self.chat_area.yview(tk.END)  # Scroll to the end

if __name__ == "__main__":
    root = tk.Tk()
    app = ChatApp(root)
    root.mainloop()
