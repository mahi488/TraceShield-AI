
import re


DETECTION_PATTERNS = {
    # Personal information
    "EMAIL": (
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    ),

    "PHONE": (
        r"(?<!\w)(?:\+91[\s-]?)?[6-9]\d{9}(?!\w)"
    ),

    "PAN": (
        r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"
    ),

    "AADHAAR_LIKE": (
        r"(?<!\d)\d{4}[\s-]?\d{4}[\s-]?\d{4}(?![\s-]?\d)"
    ),

    "IP_ADDRESS": (
        r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    ),

    # Credentials and secrets
    "PASSWORD": (
        r"""(?i)\b(?:password|passwd|pwd)\s*[:=]\s*["']?[^"'\s,;]+"""
    ),

    "API_KEY": (
        r"""(?i)\b(?:api[\s_-]?key|access[\s_-]?token|secret[\s_-]?key)\s*[:=]\s*["']?[^"'\s,;]+"""
    ),

    # Advanced sensitive information
    "CREDIT_CARD": (
        r"(?<!\d)(?:\d[ -]?){12,18}\d(?!\d)"
    ),

    "DATE_OF_BIRTH": (
        r"""(?i)\b(?:dob|date\s+of\s+birth)\s*[:=]\s*["']?\d{1,4}[-/.]\d{1,2}[-/.]\d{1,4}"""
    ),

    "AWS_ACCESS_KEY": (
        r"\bAKIA[0-9A-Z]{16}\b"
    ),

    "JWT_TOKEN": (
        r"\beyJ[A-Za-z0-9_-]*\."
        r"[A-Za-z0-9_-]+\."
        r"[A-Za-z0-9_-]+\b"
    )
}


def detect_sensitive_data(text: str) -> list:
    """Find sensitive information and remove overlapping false positives."""

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

    # Identify credit card ranges
    credit_card_ranges = [
        (item["start"], item["end"])
        for item in findings
        if item["type"] == "CREDIT_CARD"
    ]

    # Remove Aadhaar findings overlapping credit card numbers
    filtered_findings = []

    for item in findings:
        if item["type"] == "AADHAAR_LIKE":
            overlaps_card = any(
                item["start"] < card_end
                and item["end"] > card_start
                for card_start, card_end in credit_card_ranges
            )

            if overlaps_card:
                continue

        filtered_findings.append(item)

    return filtered_findings
