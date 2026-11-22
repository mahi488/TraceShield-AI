
import ipaddress
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


def is_valid_ipv4(value: str) -> bool:
    """Return True only for valid IPv4 addresses."""

    try:
        return isinstance(ipaddress.ip_address(value), ipaddress.IPv4Address)
    except ValueError:
        return False


def passes_luhn(value: str) -> bool:
    """Validate a card-shaped number using the Luhn checksum."""

    digits = [int(char) for char in value if char.isdigit()]

    if not 13 <= len(digits) <= 19:
        return False

    checksum = 0
    parity = len(digits) % 2

    for index, digit in enumerate(digits):
        if index % 2 == parity:
            digit *= 2

            if digit > 9:
                digit -= 9

        checksum += digit

    return checksum % 10 == 0


def detect_sensitive_data(text: str) -> list:
    """Find sensitive information and filter common false positives."""

    findings = []

    for category, pattern in DETECTION_PATTERNS.items():
        for match in re.finditer(pattern, text):
            value = match.group()

            if category == "IP_ADDRESS" and not is_valid_ipv4(value):
                continue

            if category == "CREDIT_CARD" and not passes_luhn(value):
                continue

            findings.append({
                "type": category,
                "value": value,
                "start": match.start(),
                "end": match.end()
            })

    # Identify all card-shaped number ranges so they are not
    # incorrectly classified as Aadhaar-like numbers.
    card_shaped_ranges = [
        (match.start(), match.end())
        for match in re.finditer(
            DETECTION_PATTERNS["CREDIT_CARD"],
            text
        )
    ]

    filtered_findings = []

    for item in findings:
        if item["type"] == "AADHAAR_LIKE":
            overlaps_card = any(
                item["start"] < card_end
                and item["end"] > card_start
                for card_start, card_end in card_shaped_ranges
            )

            if overlaps_card:
                continue

        filtered_findings.append(item)

    return filtered_findings
