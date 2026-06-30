"""
Export captions as SRT/VTT/TXT, or burn into final MP4.
"""
import os
import tempfile
import boto3
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import io
from app.core.security import get_current_user
from app.core.config import settings
from app.models.database import SessionLocal
from app.models.project import Project, CaptionSegment
from app.services.export_service import ExportService
from app.services.ffmpeg_service import FFmpegService

router = APIRouter()

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
    aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
    region_name=settings.AWS_REGION,
)


def _get_segments(db, project_id: str) -> list[dict]:
    segs = (
        db.query(CaptionSegment)
        .filter(CaptionSegment.project_id == project_id)
        .order_by(CaptionSegment.start_time)
        .all()
    )
    return [
        {"start": s.start_time, "end": s.end_time, "tanglish_text": s.tanglish_text}
        for s in segs
    ]


@router.get("/{project_id}/{fmt}")
def export_subtitles(project_id: str, fmt: str, user=Depends(get_current_user)):
    if fmt not in ("srt", "vtt", "txt"):
        raise HTTPException(400, "Format must be srt, vtt, or txt")

    db = SessionLocal()
    try:
        segments = _get_segments(db, project_id)
        if not segments:
            raise HTTPException(404, "No captions found for this project")

        content = {
            "srt": ExportService.to_srt,
            "vtt": ExportService.to_vtt,
            "txt": ExportService.to_txt,
        }[fmt](segments)

        media_type = {"srt": "application/x-subrip", "vtt": "text/vtt", "txt": "text/plain"}[fmt]
        return StreamingResponse(
            io.BytesIO(content.encode("utf-8")),
            media_type=media_type,
            headers={"Content-Disposition": f"attachment; filename=captions.{fmt}"},
        )
    finally:
        db.close()


class BurnRequest(BaseModel):
    style: dict | None = None


@router.post("/{project_id}/burn")
def burn_captions(project_id: str, payload: BurnRequest, user=Depends(get_current_user)):
    """Burns captions into the source video and uploads the result, returning a download URL."""
    db = SessionLocal()
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project or not project.video_url:
            raise HTTPException(404, "Project or source video not found")

        segments = _get_segments(db, project_id)
        if not segments:
            raise HTTPException(404, "No captions to burn")

        with tempfile.TemporaryDirectory() as tmp_dir:
            srt_path = os.path.join(tmp_dir, "captions.srt")
            with open(srt_path, "w", encoding="utf-8") as f:
                f.write(ExportService.to_srt(segments))

            video_local = os.path.join(tmp_dir, "source.mp4")
            s3_key = project.video_url.split(f"{settings.AWS_S3_BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/")[-1]
            s3_client.download_file(settings.AWS_S3_BUCKET, s3_key, video_local)

            output_path = os.path.join(tmp_dir, "captioned_output.mp4")
            FFmpegService.burn_captions(video_local, srt_path, output_path, payload.style)

            output_key = f"exports/{project_id}/captioned.mp4"
            s3_client.upload_file(output_path, settings.AWS_S3_BUCKET, output_key)

            exported_url = f"https://{settings.AWS_S3_BUCKET}.s3.{settings.AWS_REGION}.amazonaws.com/{output_key}"
            project.exported_video_url = exported_url
            db.commit()

        return {"exported_video_url": exported_url}
    finally:
        db.close()
