import re
from typing import Literal

# phrases first disambiguate intent (higher information content)
PHRASE_MEDIUM = [
    "after chemotherapy", "post chemotherapy", "after treatment", 
    "post treatment", "after chemo", "post chemo", "diet after chemo"
]
# single keywords flagged as high-risk if phrase not matched
KEYWORDS_HIGH = [
    "dose", "dosage", "prescribe", "prescription", "symptom", 
    "diagnose", "stage", "biopsy", "tumor size", "oncologist", "what treatment"
]
# general wellness triggers (non-diagnostic) — allow answer with caution
KEYWORDS_MEDIUM = [
    "diet", "nutrition", "exercise", "fatigue", "recovery", "rehabilitation",
    "mental health", "sleep"
]
# sources for high-risked cases
SOURCES = {
    "medical": [
        ("WHO — Breast Cancer Overview", "https://www.who.int/news-room/fact-sheets/detail/breast-cancer"),
        ("NCCN — Breast Cancer Guidelines (Patient)", "https://www.nccn.org/patients/guidelines/content/PDF/breast-patient.pdf"),
        ("Mayo Clinic — Breast Cancer", "https://www.mayoclinic.org/diseases-conditions/breast-cancer/symptoms-causes/syc-20352470"),
        ("American Cancer Society", "https://www.cancer.org/cancer/types/breast-cancer.html"),
    ],
    "wellness": [
        ("Cancer Research UK — Life After Treatment", "https://www.cancerresearchuk.org/about-cancer/breast-cancer/living"),
        ("BreastCancer.org — Nutrition During Recovery", "https://www.breastcancer.org/managing-life/nutrition")
    ]
}


def classify_query(query: str) -> Literal["low","medium","high"]:
    q = query.lower()

    # 1) Phrase-first: check more specific multi-word expressions first.
    for phrase in PHRASE_MEDIUM:
        if phrase in q:
            return "medium"

    # 2) Look for exact or strongly indicative high-risk keywords.
    for kw in KEYWORDS_HIGH:
        if re.search(rf"\b{re.escape(kw)}\b", q):
            return "high"

    # 3) If no high-risk, check for medium-risk keywords.
    for kw in KEYWORDS_MEDIUM:
        if re.search(rf"\b{re.escape(kw)}\b", q):
            return "medium"

    # 4) Default to low-risk (supportive/emotional).
    return "low"


def safety_response(level):
    if level == "high":
        msg = ("⚠️ I’m not a medical professional, so I can’t give diagnostic or treatment advice. "
               "For accurate medical guidance, please refer to:\n")
        srcs = SOURCES["medical"]
    elif level == "medium":
        msg = ("💡 Everyone’s recovery is different. I can share general information, "
               "but for personalized advice, consult your healthcare provider. Helpful sources:\n")
        srcs = SOURCES["wellness"]
    else:
        return None

    links = "\n".join([f"- [{name}]({url})" for name, url in srcs])
    return f"{msg}{links}"
