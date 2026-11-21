
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


GENERIC_IDENTITIES = {
    "admin",
    "administrator",
    "support",
    "info",
    "contact",
    "sales",
    "help",
    "test",
    "user",
    "root",
    "noreply",
    "no-reply",
    "service",
    "office"
}


def correlate_artifacts(artifacts: list[dict]) -> list[dict]:
    """Correlate identity evidence across multiple digital artifacts."""

    records = {}

    for artifact in artifacts:
        filename = artifact["filename"]
        text = artifact["text"]

        emails = EMAIL_PATTERN.findall(text)
        usernames = USERNAME_PATTERN.findall(text)
        has_token = bool(TOKEN_PATTERN.search(text))

        # Collect email evidence
        for email in emails:
            identity = email.split("@", 1)[0].casefold()

            if identity in GENERIC_IDENTITIES:
                continue

            record = records.setdefault(
                identity,
                {
                    "files": set(),
                    "evidence": set(),
                    "evidence_sources": {}
                }
            )

            record["files"].add(filename)
            record["evidence"].add("EMAIL")

            record["evidence_sources"].setdefault(
                "EMAIL", set()
            ).add(filename)

        # Collect username and token evidence
        for username in usernames:
            identity = username.casefold()

            if identity in GENERIC_IDENTITIES:
                continue

            record = records.setdefault(
                identity,
                {
                    "files": set(),
                    "evidence": set(),
                    "evidence_sources": {}
                }
            )

            record["files"].add(filename)
            record["evidence"].add("USERNAME")

            record["evidence_sources"].setdefault(
                "USERNAME", set()
            ).add(filename)

            if has_token:
                record["evidence"].add("SESSION_TOKEN")

                record["evidence_sources"].setdefault(
                    "SESSION_TOKEN", set()
                ).add(filename)

    correlations = []

    for identity, record in records.items():
        evidence = record["evidence"]
        files = record["files"]

        email_sources = record["evidence_sources"].get(
            "EMAIL", set()
        )

        username_sources = record["evidence_sources"].get(
            "USERNAME", set()
        )

        # Require email and username evidence in different files
        if (
            "EMAIL" in evidence
            and "USERNAME" in evidence
            and len(files) >= 2
            and email_sources
            and username_sources
            and email_sources.isdisjoint(username_sources)
        ):
            token_found = "SESSION_TOKEN" in evidence

            correlations.append({
                "matched_identity": identity[:1] + "***",
                "related_files": sorted(files),
                "evidence_types": sorted(evidence),

                "evidence_sources": {
                    evidence_type: sorted(source_files)
                    for evidence_type, source_files
                    in record["evidence_sources"].items()
                },

                "match_method": (
                    "Exact email local-part and username match"
                ),

                "identity_match_confidence": 0.90,
                "confidence_label": "HIGH",

                "risk_level": (
                    "HIGH" if token_found else "MEDIUM"
                )
            })

    return correlations
