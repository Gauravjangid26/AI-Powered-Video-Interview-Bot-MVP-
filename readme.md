# 🎥 AI-Powered Video Interview Bot – MVP

## 🧠 Objective

This MVP streamlines first-round interviews for high-volume hiring by automating:
- Role-specific greetings and question generation
- Asynchronous video recording
- AI-based transcription and evaluation

Recruiters receive structured summaries and skill assessments, allowing them to focus on top candidates.

---

## 🚀 Features

- 🎙️ AI-generated greeting and interview questions
- 🎥 Browser-based video recording using MediaRecorder API
- 📝 Transcription using OpenAI Whisper (local)
- 📊 AI-generated candidate summary and skill evaluation
- 📁 Local JSON-based storage of candidate data
- 🧑‍💼 Recruiter dashboard to view submissions and transcripts

---

## 🧰 Tech Stack

| Layer            | Technology Used                      |
|------------------|--------------------------------------|
| Frontend         | Streamlit + HTML (MediaRecorder)     |
| Backend Logic    | Python                               |
| AI Models        | gemini-1.5-flash(LLM), Whisper (STT) |
| Storage          | Local JSON (`data/submissions.json` )|
| TTS              | gTTS for greeting audio              |
| STT              | whisper                              |
---

## 📦 Folder Structure

mvp/
├── main.py                  # Streamlit app
├── requirements.txt         # Python dependencies
├── README.md                # Project documentation
├── doc.txt                  # Additional notes
├── pyproject.toml           # Optional project metadata
├── uv.lock                  # Environment lock file
├── data/
│   └── submissions.json     # Stored candidate reports
├── templates/
│   └── recorder.html        # Browser-based video recorder
├── tts_output/
│   └── *.mp3                # Generated greeting audio files
├── utils/
│   ├── llm.py                # LLM prompt logic
│   ├── stt.py                # Speech-to-text transcription
│   ├── tts.py                # Text-to-speech generation
│   └── video_audio_recorder.py # Recorder utilities
└── __pycache__/             # Compiled Python cache

---

## 🧪 Setup Instructions

### Clone the Repository

git clone https://github.com/your-username/interview-bot-mvp.git
cd interview-bot-mvp

insert api key of google in

.env

make a virtual environment

python -m venv venv
source venv/bin/activate 

Install Dependencies

pip install -r requirements.txt

 Run the App
 
streamlit run main.py


