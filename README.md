Halimoz AI Video Intelligence Summarizer
A multi-agent AI system for understanding, summarizing, and documenting video content using natural language.

Overview
AI Video Intelligence Summarizer is an AI-powered application that transforms any video into a **complete, educational understanding**.

Instead of watching long videos, users provide a video URL and receive a **well-structured summary**, with an **optional full script**, and a **downloadable PDF**, all through a ChatGPT-like interface.

---

Problem
Long-form video content presents several challenges:

• Time-consuming to watch  
• Hard to extract key ideas  
• Difficult to revisit specific explanations  
• No clean documentation format  

This leads to wasted time and inefficient learning.

---

Solution
A multi-agent AI system that:

• Extracts audio from any video URL  
• Transcribes speech automatically  
• Understands and explains the content deeply  
• Optionally generates the full script  
• Produces a clean PDF summary  

All using **free and open-source AI tools**.

---

Features

• Video URL Understanding  
Works with YouTube and supported video sources.

• Optional Script Extraction  
Users choose whether they want the full transcript or not.

• Deep Educational Summaries  
Explains ideas step-by-step, with examples and conclusions.

• Multi-Agent System  
Each agent has a dedicated responsibility:
- Video analysis
- Script generation
- Content summarization
- PDF formatting

• PDF Export  
Generates a clean, well-structured PDF based on real agent outputs.

• ChatGPT-like UI  
Modern interface with loading states and conversation flow.

• Arabic & English Support  
Works with Arabic (including dialects) and English videos.

---

Architecture

Streamlit UI  
     │  
Video Analyzer  
     │  
Whisper (Speech-to-Text)  
     │  
Multi-Agent System (CrewAI + LLaMA via Groq)  
     │  
PDF Generator  

---

💻 Installation

```bash
python -m venv venv
venv\Scripts\activate     # Windows
pip install -r requirements.txt
streamlit run app.py
```
---
## Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key_here
```
---
## ⚙️ Tech Stack

- Python  
- CrewAI  
- Whisper  
- yt-dlp  
- ReportLab  
- Streamlit  
- Groq API (LLaMA models)

---

## AI Agents

### Video Analyzer Agent
Downloads and prepares audio from the video.

### Script Agent (Optional)
Generates the full transcript when enabled by the user.

### Summary Agent
Produces a complete, structured explanation of the video.

### PDF Agent
Formats real outputs into a professional PDF.

---

## Example Use Cases

- “Summarize this 2-hour lecture.”
- “Give me a full understanding of this podcast.”
- “Extract the script and create a PDF.”
- “Explain this video as if I watched it.”

---

## Project Structure

```text
video-intelligence-summarizer/
├── app.py
├── crew.py
├── agents.py
├── tasks.py
├── llm.py
├── tools/
│   ├── video_tool.py
│   ├── whisper_tool.py
│   ├── pdf_tool.py
├── requirements.txt
├── .env.example
└── README.md
```
---
## Notes

- Transcription quality depends on audio clarity  
- Heavy dialects may slightly reduce accuracy  
- The focus is on understanding, not verbatim transcription  

---

## License

MIT License

---

## Author

Built with Mohamed Halim using CrewAI, Whisper, and open-source AI models.

