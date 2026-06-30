"""
Whisper-based Tamil speech recognition with word/segment level timestamps.
"""
import whisper
from app.core.config import settings
from functools import lru_cache


@lru_cache(maxsize=1)
def get_model():
    """Load Whisper model once and cache (expensive operation)."""
    return whisper.load_model(settings.WHISPER_MODEL, device=settings.WHISPER_DEVICE)


class WhisperService:

    @staticmethod
    def transcribe(audio_path: str, language: str = "ta") -> dict:
        """
        Transcribe Tamil audio with segment-level timestamps.

        Returns:
            {
              "language": "ta",
              "segments": [
                 {"id": 0, "start": 0.0, "end": 2.4, "text": "வணக்கம் நண்பர்களே"},
                 ...
              ]
            }
        """
        model = get_model()
        result = model.transcribe(
            audio_path,
            language=language,       # force Tamil; pass None to auto-detect
            task="transcribe",
            word_timestamps=True,
            verbose=False,
            condition_on_previous_text=True,
            temperature=0.0,
        )

        segments = []
        for seg in result["segments"]:
            segments.append({
                "id": seg["id"],
                "start": round(seg["start"], 2),
                "end": round(seg["end"], 2),
                "text": seg["text"].strip(),
                "words": [
                    {
                        "word": w["word"].strip(),
                        "start": round(w["start"], 2),
                        "end": round(w["end"], 2),
                    }
                    for w in seg.get("words", [])
                ],
            })

        return {
            "language": result.get("language", language),
            "segments": segments,
        }

    @staticmethod
    def detect_language(audio_path: str) -> str:
        """Auto-detect spoken language (used when user doesn't pre-select Tamil)."""
        model = get_model()
        audio = whisper.load_audio(audio_path)
        audio = whisper.pad_or_trim(audio)
        mel = whisper.log_mel_spectrogram(audio).to(model.device)
        _, probs = model.detect_language(mel)
        return max(probs, key=probs.get)
