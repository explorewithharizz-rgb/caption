"""
Handles extracting clean mono 16kHz WAV audio from uploaded video files
using FFmpeg, and burning final captions back into video.
"""
import ffmpeg
import os
import uuid
from app.core.config import settings


class FFmpegService:

    @staticmethod
    def extract_audio(video_path: str, output_dir: str = "/tmp") -> str:
        """Extract mono 16kHz WAV audio — optimal format for Whisper."""
        audio_path = os.path.join(output_dir, f"{uuid.uuid4()}.wav")
        (
            ffmpeg
            .input(video_path)
            .output(
                audio_path,
                ac=1,            # mono
                ar=16000,        # 16kHz sample rate
                format="wav",
                loglevel="error",
            )
            .overwrite_output()
            .run()
        )
        return audio_path

    @staticmethod
    def get_video_metadata(video_path: str) -> dict:
        probe = ffmpeg.probe(video_path)
        video_stream = next(
            (s for s in probe["streams"] if s["codec_type"] == "video"), None
        )
        return {
            "duration": float(probe["format"].get("duration", 0)),
            "width": video_stream.get("width") if video_stream else None,
            "height": video_stream.get("height") if video_stream else None,
            "fps": eval(video_stream.get("r_frame_rate", "0/1")) if video_stream else None,
            "size_bytes": int(probe["format"].get("size", 0)),
        }

    @staticmethod
    def burn_captions(video_path: str, srt_path: str, output_path: str, style: dict | None = None):
        """
        Burn an SRT file into the video as hardcoded subtitles using
        FFmpeg's subtitles filter (libass), with style overrides.
        """
        style = style or {}
        font_size = style.get("font_size", 24)
        font_name = style.get("font_family", "Arial")
        primary_color = style.get("primary_color", "&H00FFFFFF")  # white
        outline_color = style.get("outline_color", "&H00000000")  # black
        outline_width = style.get("outline_width", 2)
        alignment = style.get("alignment", 2)  # 2 = bottom center, 8 = top, 5 = mid

        force_style = (
            f"FontName={font_name},FontSize={font_size},"
            f"PrimaryColour={primary_color},OutlineColour={outline_color},"
            f"Outline={outline_width},Alignment={alignment},BorderStyle=1"
        )

        escaped_srt = srt_path.replace(":", "\\:").replace("'", "\\'")

        (
            ffmpeg
            .input(video_path)
            .output(
                output_path,
                vf=f"subtitles='{escaped_srt}':force_style='{force_style}'",
                acodec="copy",
                loglevel="error",
            )
            .overwrite_output()
            .run()
        )
        return output_path
