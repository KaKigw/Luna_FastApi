import google.generativeai as genai
import re
import json
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def generate_doctor_checklist(query: str) -> list[str]:
    """
    Generate safe doctor discussion questions using JSON format with ultra-safe fallback
    """
    
    # ULTRA-SAFE FALLBACK QUESTIONS (Option 4 safety net)
    ULTRA_SAFE_FALLBACK = [
        "• Discuss this with your healthcare team",
        "• Ask your oncologist for personalized guidance",
        "• Inquire about resources during your next appointment"
    ]
    
    # SAFETY FILTER - Immediate return for high-risk queries (Option 4 concept)
    high_risk_terms = ["dose", "medication", "treatment plan", "what should i take", "prescription"]
    if any(term in query.lower() for term in high_risk_terms):
        return [
            "• Discuss medication questions with your healthcare team",
            "• Ask your oncologist about treatment options", 
            "• Inquire about personalized medical guidance"
        ]
    
    # OPTION 1: JSON FORMAT PROMPT (Structured & Reliable)
    prompt = f"""
You are a breast cancer support assistant. Given this user question, generate 3 safe, general questions a patient could ask their doctor.

USER QUESTION: {query}

CRITICAL SAFETY RULES:
- DO NOT give medical advice
- DO NOT suggest treatments or medications
- DO NOT use words like "should", "recommend", "take"
- Questions must be general, educational, and discussion-oriented
- Use ONLY these safe starter phrases:
  * "Ask your doctor about..."
  * "Discuss with your oncologist..."
  * "Inquire about..."
  * "Bring up with your care team..."

OUTPUT AS JSON:
{{
  "questions": [
    "Ask your doctor about [general topic]",
    "Discuss with your oncologist [educational aspect]", 
    "Inquire about [related subject]"
  ]
}}

EXAMPLE FOR "side effects":
{{
  "questions": [
    "Ask your doctor about common side effects to expect",
    "Discuss with your oncologist how to monitor changes",
    "Inquire about when to contact your care team"
  ]
}}
"""
    
    try:
        model = genai.GenerativeModel("models/gemini-2.5-flash")
        response = model.generate_content(prompt)
        
        #  JSON EXTRACTION
        json_match = re.search(r'\{[^}]*"questions"[^}]*\}', response.text, re.DOTALL)
        if json_match:
            json_str = json_match.group()
            data = json.loads(json_str)
            questions = data.get("questions", [])
            
            # VALIDATE QUESTIONS ARE SAFE
            safe_questions = []
            safe_starters = ['ask your doctor about', 'discuss with your oncologist', 
                           'inquire about', 'bring up with your care team']
            
            for q in questions[:3]:  # Take max 3 questions
                q_lower = q.lower().strip()
                if any(q_lower.startswith(starter) for starter in safe_starters):
                    safe_questions.append(f"• {q.strip()}")
            
            if len(safe_questions) >= 2:  # Require at least 2 valid questions
                return safe_questions
        
        # FALLBACK: ULTRA-SAFE PARSING
        ultra_safe_prompt = f"""
USER QUESTION: "{query}"

SAFETY FIRST: Do not provide any medical advice. Only generate general discussion topics.

OUTPUT 3 ITEMS USING THESE EXACT STARTER PHRASES:
- Discuss with your healthcare team: [topic from question]
- Ask your oncologist about: [general aspect] 
- Inquire during your next appointment: [related subject]

OUTPUT FORMAT:
1. Discuss with your healthcare team: [topic]
2. Ask your oncologist about: [aspect]
3. Inquire during your next appointment: [subject]
"""
        fallback_response = model.generate_content(ultra_safe_prompt)
        
        # ULTRA-SAFE PARSING
        questions = []
        lines = fallback_response.text.strip().split("\n")
        
        for line in lines:
            line = line.strip()
            # Match numbered items with safe starters
            if re.match(r'^\d+\.', line):
                question = re.sub(r'^\d+\.\s*', '', line)
                if any(question.startswith(phrase) for phrase in [
                    "Discuss with your healthcare team:", 
                    "Ask your oncologist about:",
                    "Inquire during your next appointment:"
                ]):
                    questions.append(f"• {question}")
        
        if questions:
            return questions[:3]
            
    except Exception as e:
        print(f"Checklist generation error: {e}")
    
    # FINAL FALLBACK: Ultra-safe predefined questions
    return ULTRA_SAFE_FALLBACK

# TEST THE COMBINED APPROACH
if __name__ == "__main__":
    test_queries = [
        "What diet helps during chemotherapy?",
        "How much pain medication should I take?",
        "Managing fatigue during treatment",
        "Best exercises after mastectomy?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        checklist = generate_doctor_checklist(query)
        for item in checklist:
            print(f"  {item}")