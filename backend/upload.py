
from pathlib import Path
from typing import Annotated
import re

from fastapi import (
    APIRouter,
    UploadFile as FastAPIUploadFile,
    File,
    HTTPException
)
from fastapi.responses import FileResponse
from pydantic import WithJsonSchema

from detection_engine.extractor import extract_text
from detection_engine.detector import detect_sensitive_data
from correlation_engine.correlator import correlate_artifacts
from ai_engine.risk_classifier import classify_risk
from prevention_engine.redactor import redact_sensitive_data
from prevention_engine.file_manager import (
    save_redacted_file,
    get_redacted_file
)


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
MAX_FILES_PER_REQUEST = 10

def sanitize_filename(filename: str) -> str:
    """Remove directory components and unsafe control characters."""

    filename = filename.replace("\\", "/")
    filename = filename.rsplit("/", 1)[-1]

    filename = re.sub(r"[\x00-\x1f\x7f]", "", filename)
    filename = filename.strip(" .")

    if not filename:
        raise ValueError("Invalid filename")

    return filename[:255]


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
    if len(files) > MAX_FILES_PER_REQUEST:
        raise HTTPException(
            status_code=413,
            detail="A maximum of 10 files can be uploaded at once"
        )
    results = []
    correlation_artifacts = []

    for file in files:

        try:
            filename = sanitize_filename(file.filename or "")
        except ValueError as error:
            raise HTTPException(
                status_code=400,
                detail=str(error)
            )

        extension = Path(filename).suffix.lower()

        if extension not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail="Unsupported file type"
            )

        content = await file.read(MAX_FILE_SIZE + 1)

        if not content:
            raise HTTPException(
                status_code=400,
                detail="Uploaded file is empty"
            )

        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="File exceeds 10 MB limit"
            )

        try:
            extracted_text = extract_text(content, filename)

            findings = detect_sensitive_data(extracted_text)

            redacted_content = redact_sensitive_data(
                extracted_text,
                findings
            )

            file_id, saved_path = save_redacted_file(
                redacted_content
            )

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
            "redacted_content": redacted_content,
            "redacted_file_id": file_id,
            "download_url": f"/api/redacted/{file_id}",
            "status": "scanned, redacted and saved successfully"
        })

    correlations = correlate_artifacts(correlation_artifacts)

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


@router.get("/redacted/{file_id}")
def download_redacted_file(file_id: str):
    """Download a previously saved redacted file."""

    try:
        file_path = get_redacted_file(file_id)

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error)
        )

    except FileNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Redacted file not found"
        )

    return FileResponse(
        path=file_path,
        media_type="text/plain",
        filename=f"redacted_{file_id}.txt"
    )
