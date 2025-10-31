from rag_gemini import ask_ai
from safety import classify_query, safety_response

def chat():
    print("🌙 Breast Cancer Companion — Luna")
    print("Type your question below. Type 'quit' to exit.\n")

    while True:
        q = input("You: ")
        if q.lower() == "quit":
            print("👋 Take care. Luna is always here to support you.")
            break

        level = classify_query(q)
        warning = safety_response(level)
        if warning:
            print(f"\n⚠️ {warning}")

        response = ask_ai(q)

        if response["suppressed"]:
            print("\n🤖 Luna: I can’t provide direct medical or treatment guidance.")
            print("🔗 Trusted sources:")
            for src in response["sources"]:
                print(f"• {src['title']} — {src['url']}")
        else:
            print(f"\n🤖 Luna ({response['classification']} risk):\n{response['text']}")
            print("\n🔗 Sources used:")
            for src in response["sources"]:
                print(f"• {src['title']} — {src['url']}")

            if response["doctor_checklist"]:
                print("\n📝 Doctor checklist (suggested follow-ups):")
                for item in response["doctor_checklist"]:
                    print(f"• {item}")

        print("\n" + "-"*60 + "\n")

if __name__ == "__main__":
    chat()
