from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

# Sliding window memory: stores last 10 messages as dicts {role, content}
conversation_history = []
MAX_HISTORY = 10

def build_prompt(history, new_message):
    """Build a prompt string from conversation history + new message."""
    prompt = ""
    for entry in history:
        if entry["role"] == "user":
            prompt += f"User: {entry['content']}\n"
        else:
            prompt += f"Assistant: {entry['content']}\n"
    prompt += f"User: {new_message}\nAssistant:"
    return prompt

@app.route('/chat', methods=['POST'])
def chat():
    global conversation_history

    data = request.json
    user_input = data.get('message', '').strip()
    if not user_input:
        return jsonify({'response': 'Please enter a message.'}), 400

    # Build prompt with history
    prompt = build_prompt(conversation_history, user_input)

    response = requests.post('http://localhost:11434/api/generate', json={
        'model': 'llama3.2',
        'prompt': prompt,
        'stream': False
    })
    result = response.json()
    assistant_reply = result.get('response', '').strip()

    # Update sliding window memory
    conversation_history.append({"role": "user", "content": user_input})
    conversation_history.append({"role": "assistant", "content": assistant_reply})

    # Keep only last MAX_HISTORY messages (each exchange = 2 entries)
    if len(conversation_history) > MAX_HISTORY * 2:
        conversation_history = conversation_history[-(MAX_HISTORY * 2):]

    return jsonify({
        'response': assistant_reply,
        'history_length': len(conversation_history) // 2
    })

@app.route('/reset', methods=['POST'])
def reset():
    global conversation_history
    conversation_history = []
    return jsonify({'status': 'ok', 'message': 'Conversation reset.'})

if __name__ == '__main__':
    app.run(port=5000)