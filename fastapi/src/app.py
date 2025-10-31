from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src.rag_gemini import ask_ai
from src.report_system import report_issue


app = FastAPI()

#  Allow frontend to connect 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#  Request schema for chat
class ChatRequest(BaseModel):
    user_id: str
    query: str

#  Response schema 
class ChatResponse(BaseModel):
    response_id: str
    response_type: str
    classification: str
    suppressed: bool
    text: str
    sources: list
    doctor_checklist: list
    timestamp: str

@app.post("/chat")
async def chat_endpoint(req: ChatRequest):
    """
    Main AI entry point. Handles safety, RAG, Gemini, fallback, emotion.
    """
    try:
        result = ask_ai(req.query)
        result["user_id"] = req.user_id  # for logging
        return result
    except Exception as e:
        return {
            "response_id": "resp_error",
            "response_type": "error",
            "classification": "error",
            "suppressed": True,
            "text": f"⚠️ Internal error: {str(e)}",
            "sources": [],
            "doctor_checklist": [],
            "timestamp": None
        }

#  Feedback reporting endpoint
class ReportRequest(BaseModel):
    user_id: str
    query: str
    classification: str
    feedback: str  # "helpful", "unhelpful", "unsafe"

@app.post("/report")
async def report_endpoint(req: ReportRequest):
    """
    Logs user feedback on AI responses.
    """
    report_issue(
        user_id=req.user_id,
        query=req.query,
        classification=req.classification,
        feedback=req.feedback
    )
    return {"status": "ok", "message": "Feedback recorded"}
