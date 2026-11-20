
from io import BytesIO
from pathlib import Path
import csv
import json

from pypdf import PdfReader


def extract_pdf_text(content: bytes) -> str:
    """Extract readable text from a PDF."""
    try:
        reader = PdfReader(BytesIO(content))
        extracted_text = []

        for page in reader.pages:
            page_text = page.extract_text() or ""
            if page_text.strip():
                extracted_text.append(page_text)

        return "\n".join(extracted_text)

    except Exception as error:
        raise ValueError(f"PDF extraction failed: {error}") from error


def extract_text(content: bytes, filename: str) -> str:
    """Extract text from supported file formats."""
    extension = Path(filename).suffix.lower()

    try:
        if extension == ".pdf":
            return extract_pdf_text(content)

        text = content.decode("utf-8-sig")

        if extension in {".txt", ".log", ".py", ".js", ".java"}:
            return text

        if extension == ".csv":
            rows = list(csv.reader(text.splitlines()))
            return "\n".join(
                ", ".join(row) for row in rows
            )

        if extension == ".json":
            data = json.loads(text)
            return json.dumps(data, indent=2, ensure_ascii=False)

        raise ValueError(f"Unsupported extraction format: {extension}")

    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"Text extraction failed: {error}") from error
