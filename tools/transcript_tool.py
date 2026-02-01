from crewai.tools import BaseTool
from tools.video_tool import fetch_transcript

class TranscriptTool(BaseTool):
    name: str = "fetch_transcript"
    description: str = "Fetch full transcript from YouTube video"

    def _run(self, video_url: str) -> str:
        return fetch_transcript(video_url)
