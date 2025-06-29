# 🧠 AI Mental Health Therapist App

A conversational therapy platform that uses GPT-4o and voice AI to simulate a multilingual, emotionally intelligent therapist. This app supports journaling, mood tracking, voice interaction, and secure session storage.

## 🚀 Features

- 🧘 AI Therapist using GPT-4o and configurable therapy styles
- 🗣️ Voice input and response using ElevenLabs and Google Speech API
- 📊 Mood tracker and visualization with `mood_data.json`
- 📓 Journal management with session persistence in `sessions.json`
- 🔐 Optional encrypted storage with `.env` configuration
- 📅 Auto-deletion of old sessions (default: 30 days)
- 🌐 Multilingual support
- 🎛️ Configurable via `config.py`

---

## 📁 Project Structure

```

Mental\_health\_AI\_Therapy/
├── ai\_therapist.py          # Core AI therapy logic using GPT
├── app.py                   # Main Flask app
├── config.py                # Configuration for API keys, prompts, and constants
├── journal\_manager.py       # Handles journaling functionality
├── mood\_tracker.py          # Tracks and stores mood entries
├── mood\_data.json           # Local file for mood data
├── session\_manager.py       # Handles session logs and storage
├── sessions.json            # Stores all session entries
├── voice\_handler.py         # Voice-to-text and text-to-speech logic
├── requirements.txt         # Dependencies
├── .env                     # Environment secrets (ignored in version control)
├── README.md                # This file
├── venv/                    # Virtual environment (excluded via .gitignore)
└── **pycache**/             # Compiled cache files

````

---

## 🔧 Configuration

Create a `.env` file with the following:

```env
OPENAI_API_KEY=your-openai-key
ELEVENLABS_API_KEY=your-elevenlabs-key
GOOGLE_CLOUD_KEY=your-google-cloud-key
ENCRYPTION_KEY=your-secret-key
DATABASE_URL=sqlite:///mindcare.db
````

You can customize therapy settings in `config.py`, such as:

* `AI_MODEL` (e.g. `gpt-4o`)
* `THERAPY_APPROACHES` (CBT, DBT, ACT, etc.)
* `AUTO_DELETE_DAYS` (for old session cleanup)
* `VOICE_LANGUAGES` and `VOICE_MODEL`

---

## 🧪 Run the App

### ✅ Create and activate virtual environment

```bash
python -m venv venv
venv\Scripts\activate  # On Windows
```

### ✅ Install dependencies

```bash
pip install -r requirements.txt
```

### ✅ Start the app

```bash
python app.py
```

Then open `http://localhost:5000` in your browser or access API endpoints like `/api/session`.

---

## 📦 API Endpoints

* `GET /api/mood` – Get mood entries
* `POST /api/session` – Add a therapy session
* `GET /api/sessions` – Retrieve all sessions
* `POST /api/voice` – Process voice messages (if implemented)
* `GET /health` – Health check

---

## 🤝 Credits

Developed by **Karib Shams**
🔗 [GitHub](https://github.com/karibshams) | [LinkedIn](https://www.linkedin.com/in/karib-shams-007975305/)

---

## 📜 License

This project is for educational and non-commercial research purposes only.


```
