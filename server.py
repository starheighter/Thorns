from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app, origins=["http://localhost:8080"])

conversation_history = []
MAX_HISTORY = 10

try:
    with open("prefix.txt", "r", encoding="utf-8") as file:
        PREFIX = file.read().strip()
except FileNotFoundError:
    PREFIX = ""
    print("[WARN] prefix.txt not found – no prefix in use.")

def build_prompt(history, new_message):
    prompt = ""
    for entry in history:
        if entry["role"] == "user":
            prompt += f"User: {entry['content']}\n"
        else:
            prompt += f"Assistant: {entry['content']}\n"
    prompt += f"User: {PREFIX} {new_message}\nAssistant:"
    return prompt

@app.route('/chat', methods=['POST'])
def chat():
    global conversation_history
    data = request.json
    user_input = data.get('message', '').strip()
    if not user_input:
        return jsonify({'response': 'Please enter a message.'}), 400
    prompt = build_prompt(conversation_history, user_input)
    response = requests.post('http://localhost:11434/api/generate', json={
        'model': 'llama3.2',
        'prompt': prompt,
        'stream': False
    })
    result = response.json()
    assistant_reply = result.get('response', '').strip()
    conversation_history.append({"role": "user", "content": user_input})
    conversation_history.append({"role": "assistant", "content": assistant_reply})
    if len(conversation_history) > MAX_HISTORY * 2:
        conversation_history = conversation_history[-(MAX_HISTORY * 2):]
    return jsonify({
        'response': assistant_reply,
    })

@app.route('/reset', methods=['POST'])
def reset():
    global conversation_history
    conversation_history = []
    return jsonify({'status': 'ok', 'message': 'Conversation reset.'})

if __name__ == '__main__':
    app.run(port=5000)