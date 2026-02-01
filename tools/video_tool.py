import yt_dlp
import os
from uuid import uuid4
from tools.whisper_tool import transcribe

TEMP_DIR = "temp"
os.makedirs(TEMP_DIR, exist_ok=True)

def fetch_transcript(video_url: str) -> str:

    uid = str(uuid4())[:8]
    output = f"{TEMP_DIR}/{uid}.%(ext)s"

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192"
        }],
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([video_url])

    audio_path = f"{TEMP_DIR}/{uid}.mp3"

    if not os.path.exists(audio_path):
        raise Exception("Audio download failed")

    text = transcribe(audio_path)

    if not text.strip():
        raise Exception("Transcript empty")

    os.remove(audio_path)
    return text
