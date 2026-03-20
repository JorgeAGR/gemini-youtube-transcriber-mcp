"""
Core YouTube transcription logic using Gemini.

Library usage:
    from youtube_transcriber import transcribe_youtube
    result = transcribe_youtube("https://www.youtube.com/watch?v=...")
    # [{"timestamp": "00:00", "text": "..."}, ...]
"""

import os
from typing import Optional

from google import genai
from google.genai import types

MODEL = "gemini-3-flash-preview"

TRANSCRIPTION_PROMPT = """\
Transcribe this video's audio in full, one segment per line.

Format (single speaker):
MM:SS: <text>

Format (multiple distinguishable speakers):
MM:SS: Speaker A: <text>

Rules:
- MM:SS timestamp for every line (e.g. 00:00, 01:32, 10:45)
- One line per natural sentence or spoken segment
- Include ALL spoken content verbatim
- No headers, summaries, or blank lines — only the transcription lines"""


def transcribe_youtube(
    youtube_url: str, api_key: Optional[str] = None
) -> str:
    """
    Transcribe a YouTube video's audio using Gemini.

    Args:
        youtube_url: YouTube video URL.
        api_key: Gemini API key. Falls back to the GEMINI_API_KEY environment variable.

    Returns:
        Transcription string, one segment per line in "MM:SS: [Speaker X:] text" format.
    """
    key = api_key or os.environ.get("GEMINI_API_KEY")
    if not key:
        raise ValueError(
            "A Gemini API key is required. "
            "Set the GEMINI_API_KEY environment variable or pass api_key=."
        )

    client = genai.Client(api_key=key)

    response = client.models.generate_content(
        model=MODEL,
        contents=types.Content(
            parts=[
                types.Part(
                    file_data=types.FileData(file_uri=youtube_url),
                    video_metadata=types.VideoMetadata(fps=1 / 10),
                    media_resolution=types.MediaResolution.MEDIA_RESOLUTION_LOW,
                ),
                types.Part(text=TRANSCRIPTION_PROMPT),
            ]
        ),
        config=types.GenerateContentConfig(temperature=0.0),
    )

    if not response.text:
        raise RuntimeError("Gemini returned an empty response.")
    return response.text
