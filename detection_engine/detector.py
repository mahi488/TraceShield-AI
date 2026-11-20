
import re


DETECTION_PATTERNS = {
    "EMAIL": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",

    "PHONE": r"(?<!\w)(?:\+91[\s-]?)?[6-9]\d{9}(?!\w)",

    "PAN": r"\b[A-Z]{5}[0-9]{4}[A-Z]\b",

    "AADHAAR_LIKE": r"(?<!\d)\d{4}[\s-]?\d{4}[\s-]?\d{4}(?!\d)",

    "IP_ADDRESS": r"\b(?:\d{1,3}\.){3}\d{1,3}\b",

    "PASSWORD": r"""(?i)\b(?:password|passwd|pwd)\s*[:=]\s*["']?[^"'\s,;]+""",

    "API_KEY": r"""(?i)\b(?:api[_-]?key|access[_-]?token|secret[_-]?key)\s*[:=]\s*["']?[^"'\s,;]+"""
}


def detect_sensitive_data(text: str) -> list:
    """Find potential sensitive information in text."""

    findings = []

    for category, pattern in DETECTION_PATTERNS.items():
        matches = re.finditer(pattern, text)

        for match in matches:
            findings.append({
                "type": category,
                "value": match.group(),
                "start": match.start(),
                "end": match.end()
            })

    return findings
