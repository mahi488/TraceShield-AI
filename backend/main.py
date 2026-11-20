
from fastapi import FastAPI
from backend.upload import router as upload_router

app = FastAPI(
    title="TraceShield AI",
    description="AI-powered Cross-Artifact Privacy Leak Detection and Prevention System",
    version="1.0.0"
)

# Register the file upload module
app.include_router(upload_router, prefix="/api", tags=["File Upload"])


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
