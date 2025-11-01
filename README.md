# Luna FastAPI  
Lightweight and modular backend built with **FastAPI**, designed to handle conversational AI logic (RAG + Gemini), safety classification, and user feedback reporting.

---

## 🚀 Features  
- **Chat endpoint** using Gemini/RAG logic for contextual, safe, and intelligent responses.  
- **Feedback reporting** system for AI evaluation (helpful/unhelpful/unsafe).  
- **CORS-enabled** for easy frontend integration.  
- Modular design for future extensions (safety, post-check, emotion detection, etc.).

---

## 🧩 Tech Stack  
- **Framework:** FastAPI  
- **Language:** Python 3.11+  
- **Core modules:**  
  - `rag_gemini.py` – response generation via retrieval and Gemini.  
  - `report_system.py` – feedback logging.  
  - `safety`, `doctor_checklist`, `emotion`, etc. – internal logic (as used in other modules).  

---

## 🛠️ Installation  

### 1. Clone the repository  
```bash
git clone https://github.com/KaKigw/Luna_FastApi.git
cd Luna_FastApi
```

### 2. Create and activate a virtual environment  
```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 3. Install dependencies  
```bash
pip install -r requirements.txt
```

### 4. Run the API locally  
```bash
uvicorn src.app:app --reload
```

The server will start at [http://localhost:8000](http://localhost:8000).  
Interactive docs available at [http://localhost:8000/docs](http://localhost:8000/docs).

---

## 📡 API Endpoints  

### 1. `/chat` — POST  
**Purpose:** Main AI entry point. Handles query classification, safety, RAG, Gemini response generation, emotion detection, and fallback mechanisms.  

#### Request Body
```json
{
  "user_id": "user_001",
  "query": "What are the symptoms of low blood pressure?"
}
```

#### Response Example
```json
{
  "response_id": "resp_17459",
  "response_type": "ai",
  "classification": "medical_info",
  "suppressed": false,
  "text": "Common symptoms of low blood pressure include dizziness, fainting, and blurred vision...",
  "sources": ["https://www.healthline.com/..."],
  "doctor_checklist": ["Check hydration", "Review medications", "Monitor BP daily"],
  "timestamp": "2025-11-01T16:42:10Z"
}
```

#### Notes
- The `text` field contains the AI’s main response.  
- `sources` may list reference materials.  
- `doctor_checklist` provides structured medical advice (if applicable).  
- `suppressed: true` indicates the message was filtered for safety reasons.

---

### 2. `/report` — POST  
**Purpose:** Logs user feedback to improve AI performance and safety.  

#### Request Body
```json
{
  "user_id": "user_001",
  "query": "What are the symptoms of low blood pressure?",
  "classification": "medical_info",
  "feedback": "helpful"
}
```

#### Response Example
```json
{
  "status": "ok",
  "message": "Feedback recorded"
}
```

#### Feedback values:
- `"helpful"` — AI response was useful.  
- `"unhelpful"` — AI response was off-topic or unclear.  
- `"unsafe"` — AI response was inappropriate or unsafe.  

---

## 🗂️ Project Structure
```
Luna_FastApi/
├── src/
│   ├── app.py               # Main FastAPI app with endpoints
│   ├── rag_gemini.py        # RAG & Gemini integration logic
│   ├── report_system.py     # Logs feedback reports
│   ├── safety/              # Query safety classification
│   ├── emotion/             # Emotion detection modules
│   └── ...                  # Other support modules
├── requirements.txt         # Dependencies
├── render.yaml              # Optional: Render deployment config
└── README.md                # This file
```

---

## 🧠 Example Usage (cURL)

**Chat Example**
```bash
curl -X POST http://localhost:8000/chat      -H "Content-Type: application/json"      -d '{"user_id": "demo_user", "query": "Give me 3 relaxation techniques"}'
```

**Report Example**
```bash
curl -X POST http://localhost:8000/report      -H "Content-Type: application/json"      -d '{"user_id": "demo_user", "query": "Give me 3 relaxation techniques", "classification": "lifestyle", "feedback": "helpful"}'
```

---

## ⚙️ Deployment  
Can be deployed easily on:  
- **Render.com** (using `render.yaml`)  
- **Hugging Face Spaces**  
- **Any cloud provider** supporting FastAPI and Python 3.11+

Example Render `start command`:  
```bash
uvicorn src.app:app --host 0.0.0.0 --port 8000
```

---

## 🧾 License  
Specify your license here (e.g. MIT, Apache 2.0, etc.)

---

## ✉️ Author  
Maintainer: **KaKi**  
GitHub: [@KaKigw](https://github.com/KaKigw)
