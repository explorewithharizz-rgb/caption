"""
AI Enhancements: auto punctuation, line breaking, emoji suggestions,
and caption shortening for Shorts/Reels using an LLM (Claude/OpenAI).
Swap `call_llm` with your provider of choice.
"""
import httpx
import os

LLM_API_URL = "https://api.anthropic.com/v1/messages"
LLM_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")


async def call_llm(prompt: str, max_tokens: int = 500) -> str:
    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            LLM_API_URL,
            headers={
                "x-api-key": LLM_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-sonnet-4-6",
                "max_tokens": max_tokens,
                "messages": [{"role": "user", "content": prompt}],
            },
        )
        data = resp.json()
        return "".join(b.get("text", "") for b in data.get("content", []))


class CaptionAIService:

    @staticmethod
    async def add_punctuation_and_linebreaks(tanglish_text: str) -> str:
        prompt = (
            "Add natural punctuation and break this Tanglish (Tamil written in "
            "English letters) caption into readable lines of max 6-7 words each "
            "for a video subtitle. Keep the Tanglish spelling exactly as-is, "
            "only add punctuation and line breaks (\\n). Return only the result:\n\n"
            f"{tanglish_text}"
        )
        return await call_llm(prompt)

    @staticmethod
    async def suggest_emojis(tanglish_text: str) -> str:
        prompt = (
            "Suggest 1-3 relevant emojis that a Tamil content creator could add "
            "to this caption for Instagram Reels/YouTube Shorts. Return only the "
            f"emojis, space separated, no explanation:\n\n{tanglish_text}"
        )
        return await call_llm(prompt, max_tokens=20)

    @staticmethod
    async def shorten_for_shorts(tanglish_text: str, max_chars: int = 40) -> str:
        prompt = (
            f"Shorten this Tanglish caption to under {max_chars} characters for a "
            "fast-paced Instagram Reel/YouTube Short, keeping the meaning and "
            f"casual creator tone. Return only the shortened caption:\n\n{tanglish_text}"
        )
        return await call_llm(prompt, max_tokens=60)

    @staticmethod
    async def optimize_for_engagement(tanglish_text: str) -> str:
        prompt = (
            "Rewrite this Tanglish caption to be more engaging and hook-y for "
            "social media, while keeping it natural and in the creator's voice. "
            f"Return only the rewritten caption:\n\n{tanglish_text}"
        )
        return await call_llm(prompt, max_tokens=100)
