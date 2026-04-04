from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

from prefixhandler import generate_prefix

app = Flask(__name__)
CORS(app, origins=["http://localhost:8080"])

history = []
MAX_HISTORY = 10

def _build_prompt(user_message):
    prompt = ""
    for entry in history:
        if entry["role"] == "user":
            prompt += f"User: {entry['content']}\n"
        else:
            prompt += f"Assistant: {entry['content']}\n"
    prefix = generate_prefix(user_message)
    prompt += f"User: {prefix}\n{user_message}\nAssistant:"
    return prompt

@app.route('/chat', methods=['POST'])
def chat():
    global history
    data = request.json
    user_message = data.get('message', '').strip()
    if not user_message:
        return jsonify({'response': 'Please enter a message.'}), 400
    prompt = _build_prompt(user_message)
    response = requests.post('http://localhost:11434/api/generate', json={
        'model': 'llama3.2',
        'prompt': prompt,
        'stream': False
    })
    result = response.json()
    assistant_reply = result.get('response', '').strip()
    history.append({"role": "user", "content": user_message})
    history.append({"role": "assistant", "content": assistant_reply})
    if len(history) > MAX_HISTORY * 2:
        history = history[-(MAX_HISTORY * 2):]
    return jsonify({
        'response': assistant_reply,
    })

@app.route('/reset', methods=['POST'])
def reset():
    global history
    history = []
    return jsonify({'status': 'ok', 'message': 'Conversation reset.'})

if __name__ == '__main__':
    app.run(port=5000)