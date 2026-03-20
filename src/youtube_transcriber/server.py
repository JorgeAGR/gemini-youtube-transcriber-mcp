"""
MCP server exposing YouTube audio transcription via Gemini.

Run with:
    python -m youtube_transcriber.server

Or register in your MCP client config:
    {
      "mcpServers": {
        "youtube-transcriber": {
          "command": "python",
          "args": ["-m", "youtube_transcriber.server"],
          "env": { "GEMINI_API_KEY": "your-key-here" }
        }
      }
    }
"""

from mcp.server.fastmcp import FastMCP

from youtube_transcriber.transcriber import transcribe_youtube

mcp = FastMCP("youtube-transcriber")


@mcp.tool()
def transcribe_youtube_video(url: str) -> str:
    """
    Transcribe the audio of a YouTube video with timestamps.

    Uses Gemini to produce a line-by-line transcription. Each line is formatted as:
        [MM:SS] Transcribed text

    Args:
        url: YouTube video URL (e.g. https://www.youtube.com/watch?v=dQw4w9WgXcQ)

    Returns:
        Full timestamped transcription of the video.
    """
    return transcribe_youtube(url)


if __name__ == "__main__":
    mcp.run()
