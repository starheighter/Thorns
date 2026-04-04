# ◈ Thorns

A minimal, locally-run AI chat interface powered by [Ollama](https://ollama.com) and Flask. Thorns connects a clean, dark-themed frontend to a local LLM backend with support for modular prompt prefixing.

---

## Features

- **Fully local** — no data leaves your machine
- **Modular prompt prefixing** — dynamically inject randomized context into every prompt via `.txt` modules
- **Conversation memory** — maintains a rolling history window across turns
- **Reset endpoint** — clear conversation state via UI or API
- **Minimal, dark UI** — built with vanilla HTML/CSS/JS, no framework dependencies

---

## Project Structure

```
thorns/
├── index.html          # Frontend UI
├── styles.css          # Dark theme styles
├── script.js           # Chat logic & API calls
├── server.py           # Flask backend
├── prefixhandler.py    # Prompt prefix loader
├── requirements.txt    # Python dependencies
├── start.sh            # Launch script
└── prefix/
    └── english/        # Prefix module .txt files
```

---

## Requirements

- [Python 3.11](https://www.python.org/)
- [Ollama](https://ollama.com) with `llama3.2` pulled

### Python Dependencies

Install all required packages via the provided `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/starheighter/Thorns.git
cd Thorns

# 2. Install dependencies
pip install -r requirements.txt

# 3. Pull the Ollama model (first time only)
ollama pull llama3.2

# 4. Make the launch script executable and run it
chmod +x start.sh
./start.sh
```

Then open **http://localhost:8080** in your browser. Press `Ctrl+C` to stop all processes.

`start.sh` launches Ollama, the Flask backend, and the frontend file server in a single command, and shuts them all down cleanly when you exit.

---

## Prefix System

The `prefixhandler.py` module loads `.txt` files from `prefix/english/` and injects randomized content into the prompt before each user message. This allows you to shape the model's behavior, persona, or style without modifying the core logic.

### How it works

Each `.txt` file in `prefix/english/` contains one or more **prefix modules**, separated by `$`. One module per file is chosen at random on every request and prepended to the prompt.

### Example: `prefix/english/7.txt`

```
Convincingly show him that he is strong enough.
$
Convincingly show him that it is not necessary to be special.
$
Convincingly show him that he does not owe anything to anyone.
```

You can add as many `.txt` files as needed — each file represents an independent dimension of the prefix (e.g. tone, persona, task context).

---

## API Reference

### `POST /chat`

Send a user message and receive a model response.

**Request body:**
```json
{ "message": "Can you help me?" }
```

**Response:**
```json
{ "response": "Yes, I’m here to help. Could you tell me more about your problem?" }
```

### `POST /reset`

Clear the conversation history on the server.

**Response:**
```json
{ "status": "ok", "message": "Conversation reset." }
```

---

## Configuration

| Setting | Location | Default |
|---|---|---|
| Flask port | `server.py` | `5000` |
| Ollama model | `server.py` | `llama3.2` |
| Max history turns | `server.py` | `10` |
| CORS origin | `server.py` | `http://localhost:8080` |
| Prefix directory | `prefixhandler.py` | `prefix/english` |

---

## License

MIT