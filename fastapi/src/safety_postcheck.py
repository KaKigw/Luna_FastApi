import re

FORBIDDEN_PATTERNS = [
    r"\b\d+\s?mg\b",  # e.g. "20 mg"
    r"\byou should\b",
    r"\bdiagnos(?:e|is|ed)\b",
    r"\bconfirm(ed)?\b.*cancer"
]
# -> (bool, str)
def postcheck_and_mitigate(generated_text: str):
    for pat in FORBIDDEN_PATTERNS:
        if re.search(pat, generated_text, re.I):
            warning = (
                "⚠️ The assistant detected potentially unsafe medical content. "
                "We cannot provide diagnosis or dosing. Please consult a healthcare professional. "
                "Here are trusted sources: [ACS](https://www.cancer.org), [NCCN](https://www.nccn.org), [Mayo Clinic](https://www.mayoclinic.org)"
            )
            return False, warning
    return True, generated_text
