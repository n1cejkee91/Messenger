from flask import Flask, request
from datetime import datetime
import time

app = Flask(__name__)
messages = []
users = {}

@app.route("/")
def status():
    return {
        'status': 'OK',
        'name': 'Messenger',
        'time': datetime.now().strftime('%H:%M:%S %d/%m/%Y'),
        'users_count': len(users),
        'messages_count': len(messages)
    }

@app.route("/send_message")
def send_message():
    username = request.json['username']
    password = request.json['password']
    text = request.json['text']

    if username in users:
        if users[username] != password:
            return {'ok': False}
    else:
        users[username] = password

    messages.append({'username': username, 'text': text, 'timestamp': time.time()})

    return {'ok': True}

@app.route("/get_messages")
def get_messages():
    after = float(request.args['after'])
    print(after)
    result = []

    for message in messages:
        if message['timestamp'] > after:
            result.append(message)

    return {
        'messages': result
    }

app.run()