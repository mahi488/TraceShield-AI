
from pathlib import Path
from typing import Annotated

from fastapi import (
    APIRouter,
    UploadFile as FastAPIUploadFile,
    File,
    HTTPException
)
from pydantic import WithJsonSchema

from detection_engine.extractor import extract_text
from detection_engine.detector import detect_sensitive_data
from correlation_engine.correlator import correlate_artifacts
from ai_engine.risk_classifier import classify_risk


UploadFile = Annotated[
    FastAPIUploadFile,
    WithJsonSchema({"type": "string", "format": "binary"})
]

router = APIRouter()

ALLOWED_EXTENSIONS = {
    ".pdf", ".txt", ".csv", ".json",
    ".py", ".js", ".java", ".log"
}

MAX_FILE_SIZE = 10 * 1024 * 1024


def mask_value(value: str) -> str:
    """Mask sensitive values before returning API results."""

    if "@" in value:
        local, domain = value.split("@", 1)
        return local[:1] + "***@" + domain

    if len(value) <= 4:
        return "*" * len(value)

    return value[:2] + "*" * (len(value) - 2)


@router.post("/upload")
async def upload_files(
    files: Annotated[list[UploadFile], File(...)]
):
    results = []
    correlation_artifacts = []

    for file in files:
        filename = file.filename or ""
        extension = Path(filename).suffix.lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {filename}"
            )

        content = await file.read(MAX_FILE_SIZE + 1)

        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail=f"File exceeds 10 MB limit: {filename}"
            )

        try:
            extracted_text = extract_text(content, filename)
            findings = detect_sensitive_data(extracted_text)

            correlation_artifacts.append({
                "filename": filename,
                "text": extracted_text
            })

        except ValueError as error:
            raise HTTPException(
                status_code=400,
                detail=str(error)
            )

        safe_findings = [
            {
                "type": item["type"],
                "masked_value": mask_value(item["value"]),
                "start": item["start"],
                "end": item["end"]
            }
            for item in findings
        ]

        results.append({
            "filename": filename,
            "size_bytes": len(content),
            "extracted_characters": len(extracted_text),
            "sensitive_findings_count": len(findings),
            "findings": safe_findings,
            "status": "scanned successfully"
        })

    # Perform cross-artifact correlation
    correlations = correlate_artifacts(correlation_artifacts)

    # Calculate risk for every correlation
    for correlation in correlations:
        risk_assessment = classify_risk(
            correlation["evidence_types"],
            len(correlation["related_files"])
        )

        correlation.update(risk_assessment)

    return {
        "total_files": len(results),
        "files": results,
        "cross_artifact_correlations": correlations,
        "total_correlations": len(correlations)
    }
