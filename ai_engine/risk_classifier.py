
RISK_WEIGHTS = {
    "EMAIL": 1,
    "USERNAME": 1,
    "PHONE": 2,
    "IP_ADDRESS": 2,
    "PAN": 3,
    "AADHAAR_LIKE": 3,
    "CREDIT_CARD": 4,
    "DATE_OF_BIRTH": 2,
    "PASSWORD": 4,
    "API_KEY": 4,
    "AWS_ACCESS_KEY": 5,
    "JWT_TOKEN": 4,
    "SESSION_TOKEN": 4,
}


REMEDIATION_ACTIONS = {
    "EMAIL": "Limit unnecessary exposure of email addresses.",
    "USERNAME": "Review exposed usernames and restrict public access.",
    "PHONE": "Remove or mask exposed phone numbers.",
    "IP_ADDRESS": "Review IP address exposure and access restrictions.",
    "PAN": "Secure exposed PAN information and restrict access.",
    "AADHAAR_LIKE": "Mask Aadhaar-like numbers and restrict access.",
    "CREDIT_CARD": "Secure exposed card information and contact the card issuer.",
    "DATE_OF_BIRTH": "Mask exposed dates of birth and restrict access.",
    "PASSWORD": "Change exposed passwords immediately.",
    "API_KEY": "Revoke and rotate exposed API keys.",
    "AWS_ACCESS_KEY": "Disable exposed AWS credentials and rotate access keys.",
    "JWT_TOKEN": "Invalidate exposed JWT tokens and review active sessions.",
    "SESSION_TOKEN": "Invalidate exposed session tokens immediately.",
}


def classify_risk(
    evidence_types: list[str],
    related_file_count: int
) -> dict:
    """Calculate explainable privacy risk and remediation guidance."""

    unique_evidence = set(evidence_types)

    score = sum(
        RISK_WEIGHTS.get(evidence, 0)
        for evidence in unique_evidence
    )

    explanations = []

    for evidence in sorted(unique_evidence):
        if evidence in RISK_WEIGHTS:
            explanations.append(
                f"{evidence} exposure detected"
            )

    if related_file_count >= 3:
        score += 2
        explanations.append(
            "Information is connected across three or more files."
        )
    elif related_file_count >= 2:
        score += 1
        explanations.append(
            "Information is connected across multiple files."
        )

    if score >= 9:
        risk_level = "CRITICAL"
    elif score >= 5:
        risk_level = "HIGH"
    elif score >= 3:
        risk_level = "MEDIUM"
    else:
        risk_level = "LOW"

    if not explanations:
        explanations.append(
            "No recognized sensitive evidence found."
        )

    recommended_actions = [
        REMEDIATION_ACTIONS[evidence]
        for evidence in sorted(unique_evidence)
        if evidence in REMEDIATION_ACTIONS
    ]

    if related_file_count >= 2:
        recommended_actions.append(
            "Review all related files for connected privacy exposure."
        )

    if risk_level in {"HIGH", "CRITICAL"}:
        recommended_actions.append(
            "Prioritize remediation and review the security incident."
        )

    if not recommended_actions:
        recommended_actions.append(
            "Continue monitoring and perform regular security scans."
        )

    return {
        "risk_score": score,
        "risk_level": risk_level,
        "explanations": explanations,
        "recommended_actions": recommended_actions
    }
