import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def detect_emotion(text: str) -> str:
    prompt = f"""
Classify the emotion of this message as one of:
["neutral", "sad", "anxious", "angry", "hopeful", "confused"]

Message: {text}
"""
    model = genai.GenerativeModel("models/gemini-2.5-flash")
    response = model.generate_content(prompt)
    emo = response.text.strip().lower()

    return emo if emo in ["neutral", "sad", "anxious", "angry", "hopeful", "confused"] else "neutral"
