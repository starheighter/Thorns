const chatArea = document.getElementById('chatArea');
const input = document.getElementById('myInput');
const sendBtn = document.getElementById('sendBtn');
const resetBtn = document.getElementById('resetBtn');

input.addEventListener('input', () => {
    input.style.height = 'auto';
    input.style.height = Math.min(input.scrollHeight, 140) + 'px';
});

input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        chat();
    }
});

resetBtn.addEventListener('click', async () => {
    try {
        await fetch('http://localhost:5000/reset', { method: 'POST' });
    } catch (_) { }
    chatArea.innerHTML = `
    <div class="welcome" id="welcome">
      <div class="welcome-icon">◈</div>
      <h1>HOW ARE YOUR ?</h1>
    </div>`;
});

function removeWelcome() {
    const welcome = document.getElementById('welcome');
    if (welcome) welcome.remove();
}

function addMessage(role, text) {
    const row = document.createElement('div');
    row.className = `message-row ${role}`;

    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    bubble.textContent = text;

    row.appendChild(bubble);
    chatArea.appendChild(row);
    chatArea.scrollTop = chatArea.scrollHeight;
    return row;
}

function addTypingIndicator() {
    const row = document.createElement('div');
    row.className = 'message-row bot';
    row.id = 'typing';
    row.innerHTML = `
    <div class="typing-bubble">
      <span class="typing-dot"></span>
      <span class="typing-dot"></span>
      <span class="typing-dot"></span>
    </div>`;
    chatArea.appendChild(row);
    chatArea.scrollTop = chatArea.scrollHeight;
}

function removeTypingIndicator() {
    const t = document.getElementById('typing');
    if (t) t.remove();
}

async function chat() {
    const userMessage = input.value.trim();
    if (!userMessage) return;
    removeWelcome();
    addMessage('user', userMessage);
    input.value = '';
    input.style.height = 'auto';
    sendBtn.disabled = true;
    addTypingIndicator();
    try {
        const response = await fetch('http://localhost:5000/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: userMessage })
        });
        const data = await response.json();
        removeTypingIndicator();
        addMessage('bot', data.response);
    } catch (error) {
        removeTypingIndicator();
        addMessage('bot', 'Connection to server failed. Is the server running on port 5000?');
    } finally {
        sendBtn.disabled = false;
        input.focus();
    }
}