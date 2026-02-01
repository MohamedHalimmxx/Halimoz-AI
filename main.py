from fastapi import FastAPI
from pydantic import BaseModel
from crew import run_crew

app = FastAPI()

class VideoRequest(BaseModel):
    url: str
    include_script: bool = True

@app.post("/summarize")
def summarize_video(req: VideoRequest):
    return run_crew(req.url)
