def redact_sensitive_data(
    text: str,
    findings: list[dict]
) -> str:
    """Replace detected sensitive values with redaction labels."""

    valid_spans = []

    for finding in findings:
        start = finding.get("start")
        end = finding.get("end")
        value = finding.get("value")
        category = finding.get("type")

        if not isinstance(start, int) or not isinstance(end, int):
            continue

        if not isinstance(value, str) or not isinstance(category, str):
            continue

        if start < 0 or end > len(text) or start >= end:
            continue

        if text[start:end] != value:
            continue

        valid_spans.append((start, end, category))

    valid_spans.sort(
        key=lambda item: (item[0], -(item[1] - item[0]))
    )

    selected_spans = []

    for span in valid_spans:
        start, end, category = span

        overlaps = any(
            start < selected_end and end > selected_start
            for selected_start, selected_end, _ in selected_spans
        )

        if not overlaps:
            selected_spans.append(span)

    for start, end, category in sorted(
        selected_spans,
        key=lambda item: item[0],
        reverse=True
    ):
        text = (
            text[:start]
            + f"[REDACTED:{category}]"
            + text[end:]
        )

    return text