"""
Tanglish Caption AI - FastAPI Backend Entry Point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import upload, transcribe, captions, export, auth, projects, admin

app = FastAPI(
    title="Tanglish Caption AI API",
    description="Backend for Tamil speech -> Tanglish caption generation",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(upload.router, prefix="/api/upload", tags=["upload"])
app.include_router(transcribe.router, prefix="/api/transcribe", tags=["transcribe"])
app.include_router(captions.router, prefix="/api/captions", tags=["captions"])
app.include_router(export.router, prefix="/api/export", tags=["export"])
app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
app.include_router(admin.router, prefix="/api/admin", tags=["admin"])


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "tanglish-caption-ai"}
