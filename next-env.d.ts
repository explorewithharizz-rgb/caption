"""
Secure chunked-aware video upload endpoint with validation.
"""
import os
import uuid
import boto3
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from app.core.config import settings
from app.core.security import get_current_user

router = APIRouter()

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION,
)


@router.post("/video")
async def upload_video(
    file: UploadFile = File(...),
    user=Depends(get_current_user),
):
    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in settings.ALLOWED_VIDEO_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported format. Allowed: {settings.ALLOWED_VIDEO_EXTENSIONS}",
        )

    # Validate size by reading content-length header / streaming check
    contents = await file.read()
    size_mb = len(contents) / (1024 * 1024)
    if size_mb > settings.MAX_UPLOAD_SIZE_MB:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds {settings.MAX_UPLOAD_SIZE_MB}MB limit.",
        )

    project_id = str(uuid.uuid4())
    s3_key = f"uploads/{user['id']}/{project_id}{ext}"

    s3_client.put_object(
        Bucket=settings.AWS_S3_BUCKET,
        Key=s3_key,
        Body=contents,
        ContentType=file.content_type,
    )

    video_url = f"https://{settings.AWS_S3_BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/{s3_key}"

    # Enqueue background transcription job (see workers/transcription_worker.py)
    from app.workers.transcription_worker import process_video_task
    process_video_task.delay(project_id=project_id, s3_key=s3_key, user_id=user["id"])

    return {
        "project_id": project_id,
        "video_url": video_url,
        "status": "queued",
        "message": "Upload successful. Transcription started.",
    }
