
from flask import Flask, request
import requests
import json
import os

app = Flask(__name__)

VERIFY_TOKEN = os.environ.get("123456")
ACCESS_TOKEN = os.environ.get("EAAHxZBwndBV0BOZCkRHAfkGgWR0MIOgbMDiSv1gGvwNxiWWgEXoO9qQeupZBEO1HcnmZABOgdXfDF1aRDqJm0rxO9QrzmKPZBvofRRZCx1ZCJazjz2HKy3a2yCL5ZBQYcx1QMk8kKC9umNZBFKJXd45PhpdZBS0mG4kP1YvZALZCuWzT1Gd2n2dRveeP7baXzCzfFC6fZBgZDZD")
PHONE_NUMBER_ID = os.environ.get("9440200009396701")

@app.route('/webhook', methods=['GET'])
def verify():
    if request.args.get("hub.verify_token") == VERIFY_TOKEN:
        return request.args.get("hub.challenge")
    return "Token inválido", 403

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Mensaje recibido:", json.dumps(data, indent=2))

    try:
        message = data['entry'][0]['changes'][0]['value']['messages'][0]
        number = message['from']
        text = message['text']['body']
        send_message(number, f"Hola, escribiste: {text}")
    except Exception as e:
        print("Error:", e)

    return 'ok', 200

def send_message(to, message):
    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        'Authorization': f'Bearer {ACCESS_TOKEN}',
        'Content-Type': 'application/json'
    }
    payload = {
        "messaging_product": "whatsapp",
        "to": to,
        "text": {"body": message}
    }
    response = requests.post(url, headers=headers, json=payload)
    print("Respuesta:", response.json())

if __name__ == "__main__":
    app.run()
