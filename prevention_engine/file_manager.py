
from pathlib import Path
from uuid import uuid4
import re


PROJECT_ROOT = Path(__file__).resolve().parent.parent

REDACTED_DIRECTORY = (
    PROJECT_ROOT / "storage" / "redacted"
)


def save_redacted_file(content: str) -> tuple[str, Path]:
    """Save redacted text using a unique file ID."""

    REDACTED_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True
    )

    file_id = uuid4().hex

    file_path = REDACTED_DIRECTORY / f"{file_id}.txt"

    file_path.write_text(
        content,
        encoding="utf-8"
    )

    return file_id, file_path


def get_redacted_file(file_id: str) -> Path:
    """Retrieve a redacted file using its unique ID."""

    if not re.fullmatch(r"[a-f0-9]{32}", file_id):
        raise ValueError("Invalid redacted file ID")

    file_path = REDACTED_DIRECTORY / f"{file_id}.txt"

    if not file_path.is_file():
        raise FileNotFoundError("Redacted file not found")

    return file_path
