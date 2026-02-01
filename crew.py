from dotenv import load_dotenv
import os
from crewai import Agent, Task, Crew, Process, LLM
from tools.transcript_tool import TranscriptTool

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    temperature=0.3,
    api_key=api_key
)

script_agent = Agent(
    role="Transcription Agent",
    goal="Extract full transcript from YouTube videos",
    backstory="Expert in audio transcription",
    tools=[TranscriptTool()],
    llm=llm,
    verbose=True
)

summary_agent = Agent(
    role="Expert Detail-oriented educator, analyst and content summarizer",
    goal="""
          Produce a complete, deep understanding of video content.
          Summarize the following content so the reader feels they have fully watched the video.
          The summary should have the following Structure:
              Title
              Overview
              Main Sections
              Key Takeaways
              Final Conclusion
        """,
    backstory="You specialize in explaining complex ideas clearly and thoroughly.",
    llm=llm,
    verbose=True

)


def run_crew(video_url: str):

    script_task = Task(
        description=f"Use fetch_transcript to get full transcript from {video_url}",
        expected_output="Raw transcript text",
        agent=script_agent
    )

    summary_task = Task(
        description="""
        produce a COMPLETE summary of the video transcript
        such that the reader feels they have fully watched the video.

        Guidelines:
        - Preserve the logical flow of the video.
        - Explain ideas clearly and deeply.
        - Include examples, analogies, and conclusions where relevant.
        - If the speaker explains a process, rewrite it step-by-step.
        - If opinions are expressed, reflect them neutrally.
        - Do NOT mention timestamps.
        - Do NOT mention that this is a summary.

        Output format (STRICT):
           Title
           Overview
           Main Sections
           Key Takeaways (bullets)
           Conclusion
           """,
        expected_output="Full Detailed Structured planation of the video content",
        agent=summary_agent,
        context=[script_task]
    )

    crew = Crew(
        agents=[script_agent, summary_agent],
        tasks=[script_task, summary_task],
        process=Process.sequential
    )

    result = crew.kickoff()

    return {
        "summary": result.raw,
        "script": script_task.output.raw
    }


#streamlit run app.py