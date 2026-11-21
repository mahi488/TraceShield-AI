
from io import BytesIO, StringIO
from pathlib import Path
import csv
import json

from pypdf import PdfReader


def extract_pdf_text(content: bytes) -> str:
    """Extract readable text from a PDF."""

    try:
        reader = PdfReader(BytesIO(content))
        extracted_text = []

        if reader.is_encrypted:
            raise ValueError("Encrypted PDF files are not supported")

        for page in reader.pages:
            page_text = page.extract_text() or ""

            if page_text.strip():
                extracted_text.append(page_text)

        return "\n".join(extracted_text)

    except ValueError:
        raise

    except Exception as error:
        raise ValueError(
            "PDF extraction failed. The file may be damaged or invalid."
        ) from error


def extract_text(content: bytes, filename: str) -> str:
    """Extract text from supported file formats."""

    if not content:
        raise ValueError("Uploaded file is empty")

    extension = Path(filename).suffix.lower()

    try:
        if extension == ".pdf":
            return extract_pdf_text(content)

        text = content.decode("utf-8-sig")

        if extension in {".txt", ".log", ".py", ".js", ".java"}:
            return text

        if extension == ".csv":
            rows = list(
                csv.reader(
                    StringIO(text),
                    strict=True
                )
            )

            return "\n".join(
                ", ".join(row) for row in rows
            )

        if extension == ".json":
            data = json.loads(text)

            return json.dumps(
                data,
                indent=2,
                ensure_ascii=False
            )

        raise ValueError(
            f"Unsupported extraction format: {extension}"
        )

    except UnicodeDecodeError as error:
        raise ValueError(
            "Text extraction failed: unsupported text encoding"
        ) from error

    except json.JSONDecodeError as error:
        raise ValueError(
            "Text extraction failed: invalid JSON format"
        ) from error

    except csv.Error as error:
        raise ValueError(
            "Text extraction failed: invalid CSV format"
        ) from error
