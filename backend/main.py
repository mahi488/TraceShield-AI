
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.upload import router as upload_router

app = FastAPI(
    title="TraceShield AI",
    description="AI-powered Cross-Artifact Privacy Leak Detection and Prevention System",
    version="1.0.0"
)

# Allow the React frontend to communicate with FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5174",
        "http://localhost:5175",
        "http://127.0.0.1:5175",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Register the file upload module
app.include_router(
    upload_router,
    prefix="/api",
    tags=["File Upload"]
)


@app.get("/")
def home():
    return {
        "project": "TraceShield AI",
        "message": "Backend is running successfully!",
        "status": "active"
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
