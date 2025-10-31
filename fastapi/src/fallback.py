from src.retriever import retrieve_context

FALLBACK_SOURCES = [
    "https://www.who.int/health-topics/cancer",
    "https://www.cancer.gov/about-cancer/treatment/side-effects",
    "https://www.nccn.org/patientresources/patient-resources/guidelines-for-patients"
]

def fallback_response(query: str) -> dict:
    retrieved = retrieve_context(query, top_k=2)
    extra_links = [doc["url"] for doc in retrieved if doc.get("url")]

    return {
        "response_id": "resp_fallback",
        "classification": "fallback",
        "suppressed": False,
        "text": (
            "⚠️ I wasn’t able to provide a personalized answer safely. "
            "Here are reliable resources you can check:"
        ),
        "sources": FALLBACK_SOURCES + extra_links,
        "doctor_checklist": [],
        "timestamp": None  # will be added by caller
    }
