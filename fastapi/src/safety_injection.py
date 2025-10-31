import re

INJECTION_PATTERNS = [
    r"ignore previous instructions",
    r"pretend to be",
    r"you are now",
    r"disregard all rules",
    r"act as",
    r"jailbreak",
    r"system prompt"
]

def detect_prompt_injection(text: str) -> bool:
    for pat in INJECTION_PATTERNS:
        if re.search(pat, text, re.I):
            return True
    return False
