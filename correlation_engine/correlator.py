
import re


EMAIL_PATTERN = re.compile(
    r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
)

USERNAME_PATTERN = re.compile(
    r"""(?i)["']?(?:username|user|login|account)["']?\s*[:=]\s*["']?([A-Za-z0-9._-]+)"""
)

TOKEN_PATTERN = re.compile(
    r"""(?i)["']?(?:session[_-]?token|access[_-]?token)["']?\s*[:=]\s*["']?([A-Za-z0-9._~+/=-]{8,})"""
)


def correlate_artifacts(artifacts: list[dict]) -> list[dict]:
    """Find identities connected across multiple files."""

    records = {}

    for artifact in artifacts:
        filename = artifact["filename"]
        text = artifact["text"]

        emails = EMAIL_PATTERN.findall(text)
        usernames = USERNAME_PATTERN.findall(text)
        has_token = bool(TOKEN_PATTERN.search(text))

        # Use email local parts as identity candidates.
        for email in emails:
            identity = email.split("@", 1)[0].casefold()

            record = records.setdefault(
                identity,
                {"files": set(), "evidence": set()}
            )

            record["files"].add(filename)
            record["evidence"].add("EMAIL")

        # Match explicit usernames with email local parts.
        for username in usernames:
            identity = username.casefold()

            record = records.setdefault(
                identity,
                {"files": set(), "evidence": set()}
            )

            record["files"].add(filename)
            record["evidence"].add("USERNAME")

            # Associate a token with the username in the same artifact.
            if has_token:
                record["evidence"].add("SESSION_TOKEN")

    correlations = []

    for identity, record in records.items():
        evidence = record["evidence"]
        files = record["files"]

        if (
            "EMAIL" in evidence
            and "USERNAME" in evidence
            and len(files) >= 2
        ):
            correlations.append({
                "matched_identity": identity[:1] + "***",
                "related_files": sorted(files),
                "evidence_types": sorted(evidence),
                "risk_level": (
                    "HIGH"
                    if "SESSION_TOKEN" in evidence
                    else "MEDIUM"
                )
            })

    return correlations

