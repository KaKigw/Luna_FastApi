import os
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime, timezone
import numpy as np


from src.retriever import retrieve_context
from src.safety import classify_query
from src.safety_postcheck import postcheck_and_mitigate
from src.safety_phi import scrub_phi
from src.safety_injection import detect_prompt_injection
from src.doctor_checklist import generate_doctor_checklist
from src.emotion_detector import detect_emotion
from src.fallback import fallback_response

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

TONE_PREFIX = {
    "sad": " I’m sorry this feels difficult.",
    "anxious": " I understand this can be worrying.",
    "angry": " Let’s take this one step at a time.",
    "hopeful": " That’s a great step forward!",
    "confused": " Let’s try to clarify this together.",
    "neutral": ""
}

def ask_ai(query):
    query_clean = scrub_phi(query)

    # Prompt injection defense
    if detect_prompt_injection(query_clean):
        fallback = fallback_response(query_clean)
        fallback["timestamp"] = datetime.now(timezone.utc).isoformat()
        return fallback
    
    #  Classification and context retrieval
    classification = classify_query(query_clean)
    hits = retrieve_context(query_clean, top_k=3)

    # No relevant chunks → fallback
    if not hits:
        fallback = fallback_response(query_clean)
        fallback["timestamp"] = datetime.now(timezone.utc).isoformat()
        return fallback
    
    sources_text = "\n".join([
        f"{i+1}) {h['title']} — {h['url']}" for i, h in enumerate(hits)
    ])
    excerpts = "\n\n".join([
        f"EXCERPT {i+1}:\n{h['excerpt']}" for i, h in enumerate(hits)
    ])

    system_instructions = """
You are an educational assistant for breast cancer support.
- NEVER provide medical diagnosis or prescribe medication.
- You MAY provide general, evidence-based educational information.
- Always append: "This is educational only — consult a clinician for personalized advice."
- When using facts, cite the source by name in parentheses, e.g., (Mayo Clinic).
- If classification is 'high', refuse to answer medical/treatment questions and only provide source links.
- If classification is 'medium', prepend a one-line caution and then provide a general answer using ONLY the supplied excerpts.
- Avoid repeating the same sentence or phrase multiple times.
- Use at most the supplied excerpts; do not invent facts.
"""

    prompt = f"""
{system_instructions}

USER_QUERY_CLASSIFICATION: {classification}
SOURCES:
{sources_text}

EXCERPTS:
{excerpts}

USER_QUESTION: {query_clean}

REPLY_INSTRUCTIONS:
- Follow the rules above.
- Keep answer concise (3–6 sentences).
- After the answer include "SOURCES:" and list the titles and URLs you used.
"""

    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(prompt)
        safe, final_text = postcheck_and_mitigate(response.text.strip())
    except Exception:
        fallback = fallback_response(query_clean)
        fallback["timestamp"] = datetime.now(timezone.utc).isoformat()
        fallback["response_type"] = "fallback"
        return fallback

    #  Emotion detection
    emotion = detect_emotion(query_clean)
    tone_prefix = TONE_PREFIX.get(emotion, "")
    final_text = tone_prefix + " " + final_text

    #  Final structured response
    return {
        "response_id": f"resp_{np.random.randint(10000)}",
        "response_type": "gemini",
        "classification": classification,
        "suppressed": not safe,
        "text": final_text,
        "sources": hits,
        "doctor_checklist": generate_doctor_checklist(query_clean) if classification == "medium" else [],
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
