# TraceShield AI

### An AI-Powered Cross-Artifact Privacy Leak Detection and Prevention System

TraceShield AI is a cybersecurity project designed to identify sensitive information exposed across multiple digital artifacts.

It scans uploaded files, detects sensitive information, identifies potential relationships between artifacts, evaluates security risk, and generates redacted files to help prevent privacy leakage.

> **Note:** Risk classification and cross-artifact correlation currently use explainable rule-based logic and heuristics.

## Features

- Multi-file scanning
- Sensitive information detection
- Email address detection
- Indian phone number detection
- PAN and Aadhaar-like number detection
- IP address detection
- Password and API key detection
- Credit card candidate validation
- Date of birth detection
- AWS access key detection
- JWT token detection
- Cross-artifact identity correlation
- Rule-based risk classification
- Sensitive information redaction
- Redacted file storage and download
- FastAPI backend
- React-based frontend

## Supported File Formats

- PDF (`.pdf`)
- Text (`.txt`)
- CSV (`.csv`)
- JSON (`.json`)
- Python (`.py`)
- JavaScript (`.js`)
- Java (`.java`)
- Log (`.log`)

## Technology Stack

### Backend
- Python
- FastAPI
- Uvicorn
- PyPDF

### Frontend
- React
- Vite
- Tailwind CSS
- Framer Motion
- Axios
- Recharts
- Lucide React

### Testing
- Pytest

### Development Environment
- Windows
- Visual Studio Code
- PowerShell

## Project Architecture

```text
TraceShield-AI/
├── ai_engine/
│   └── risk_classifier.py
├── backend/
│   ├── main.py
│   └── upload.py
├── correlation_engine/
│   └── correlator.py
├── detection_engine/
│   ├── detector.py
│   └── extractor.py
├── prevention_engine/
│   ├── redactor.py
│   └── file_manager.py
├── frontend/
│   └── src/
│       ├── components/
│       └── services/
├── sample_data/
├── storage/
│   └── redacted/
├── tests/
├── requirements.txt
└── README.md
```

## Installation

Clone the repository:

```bash
git clone https://github.com/mahi488/TraceShield-AI.git
cd TraceShield-AI
```

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install backend dependencies:

```powershell
pip install -r requirements.txt
```

Install frontend dependencies:

```powershell
cd frontend
npm install
cd ..
```

## Running the Backend

From the project root, activate the virtual environment and run:

```powershell
python -m uvicorn backend.main:app --reload
```

Backend URL: http://127.0.0.1:8000

API documentation: http://127.0.0.1:8000/docs

Health check: http://127.0.0.1:8000/health

## Running the Frontend

Open a second PowerShell terminal:

```powershell
cd frontend
npm run dev
```

Open the local URL displayed by Vite in your browser.

The frontend communicates with the backend using the API URL configured in `frontend/.env`.

## How It Works

1. The user uploads one or more supported files.
2. The backend extracts readable file content.
3. The detection engine searches for sensitive information.
4. The correlation engine identifies potential relationships across uploaded artifacts.
5. The risk classifier assigns an explainable risk level.
6. The prevention engine redacts detected sensitive information.
7. Redacted files are saved and made available for download.
8. The frontend displays scanning findings and risk information.

## Security Considerations

- Uploaded files are subject to file type and size restrictions.
- Sensitive values are masked in finding summaries.
- Redacted content is generated before download.
- Cross-artifact matches indicate potential relationships, not proof of identity or token ownership.
- Risk classification is rule-based and explainable; it is not a trained machine-learning model.
- This project is a cybersecurity demonstration and should undergo additional security testing before production deployment.

## Running Tests

From the project root:

```powershell
python -m pytest -v
```

Check dependency consistency:

```powershell
python -m pip check
```
