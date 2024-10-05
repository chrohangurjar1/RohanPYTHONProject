from flask import Flask, request, jsonify
import requests
import re
import os

app = Flask(__name__)


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
            (r'what do you think about (.*)\?', "I think {0} is interesting!"),
            (r'what is the weather like in (.*)\?',
             "I don't have real-time weather updates, but I hope it's nice in {0}!"),
        ]

    def get_response(self, user_input):
        for pattern, response in self.responses:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                if '{0}' in response:
                    return response.format(match.group(1))
                return response
        return "Sorry, I don't understand that."


chatbot = Chatbot()


@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json

    # Handle incoming media
    if 'messages' in data and len(data['messages']) > 0:
        message = data['messages'][0]

        if 'text' in message:
            message_text = message['text']['body']
            sender_number = message['from']
            response_text = chatbot.get_response(message_text)
            print(f"Received message from {sender_number}: {message_text}")
            print(f"Response: {response_text}")
            send_message(sender_number, response_text)

        elif 'image' in message:
            image_id = message['image']['id']
            sender_number = message['from']
            # Here you can implement logic to handle images if needed
            response_text = "I received an image. Currently, I cannot process it."
            print(f"Received image from {sender_number} with ID: {image_id}")
            send_message(sender_number, response_text)

    return jsonify({"status": "success"}), 200


def send_message(to, message):
    url = "https://api.whatsapp.com/send"  # Replace with your WhatsApp API endpoint
    payload = {
        "to": to,
        "type": "text",
        "text": {
            "body": message
        }
    }
    headers = {
        "Authorization": "Bearer YOUR_ACCESS_TOKEN",  # Replace with your access token
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()


if __name__ == '__main__':
    app.run(port=5000)
