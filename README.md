---

# 🌙 Luna FastAPI Backend

Modular FastAPI backend powering **LunaVoice** — designed for clarity, reproducibility, and patient-centered deployment. Built for hackathon teams and scalable health tools.

---

## 🚀 Quickstart

### 1. Clone the repository

Clone the repo and navigate into the project folder:

```
git clone https://github.com/KaKigw/Luna_FastApi.git
cd Luna_FastApi
```

### 2. Install dependencies

Install required Python packages:

```
pip install -r requirements.txt
```

### 3. Run locally

Start the FastAPI server:

```
uvicorn fastapi.src.app:app --reload
```

Visit `http://localhost:8000/docs` to explore the Swagger UI.

---

## 🧠 API Overview

| Endpoint           | Method | Description                                      |
|--------------------|--------|--------------------------------------------------|
| `/generate_voice`  | POST   | Converts input text to speech using Hugging Face TTS |
| `/summarize_text`  | POST   | Summarizes input text using Gemini RAG          |
| `/health_check`    | GET    | Confirms API is running                         |

All endpoints accept and return JSON. Swagger UI provides schemas and testing interface.

---

## 🧩 Folder Structure

```
Luna_FastApi/
├── fastapi/
│   └── src/
│       ├── app.py          # Main FastAPI app
│       ├── rag_gemini.py   # Gemini-based summarization logic
│       ├── tts_helpers.py  # TTS generation and caching
├── requirements.txt        # Dependencies (must be in root for HF Spaces)
```

---

## ☁️ Deployment Notes

### ✅ Hugging Face Spaces

LunaVoice is deployed on Hugging Face Spaces using the FastAPI SDK.

**Setup requirements:**
- SDK: `fastapi`
- Entry point: `fastapi/src/app.py`
- Python version: `3.11.9` (for FAISS compatibility)
- `requirements.txt` must be in the root directory

### ❌ Render

Deployment to Render failed due to memory limitations. The free tier provides only **512MB RAM**, which was exceeded during runtime. Hugging Face Spaces is recommended for lightweight deployment.

---

## 🧪 Example Payloads

### `/generate_voice`

```json
{
  "text": "Hello Luna, how are you today?"
}
```

### `/summarize_text`

```json
{
  "text": "Breast cancer is a disease in which cells in the breast grow out of control..."
}
```

---

## 🛠 Troubleshooting

- `ModuleNotFoundError`: Check import paths and repo structure
- `HF TTS errors`: Ensure valid Hugging Face token and model availability
- `Deployment fails`: Validate memory usage and environment setup

---

## 👥 Team Notes

- Modularized for easy handoff and extension
- Annotated functions for clarity and onboarding
- Designed with older adults in mind — prioritize comfort, clarity, and accessibility
- Reproducible setup for hackathon teams and future scaling

---

## 📬 Contact

For questions or contributions, open an issue or fork the repo on GitHub.

---

Let me know if you want to add Gemini chunking strategy, caching logic, or a Hugging Face README for the Spaces UI.
