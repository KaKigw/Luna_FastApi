from rag_gemini import ask_ai

query = "My name is Sarah and I was diagnosed on 10/10/2023. What diet helps after chemotherapy?"
response = ask_ai(query)
print(response["classification"])
print(response["doctor_checklist"])
print(response["text"])

