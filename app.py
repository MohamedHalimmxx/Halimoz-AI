import streamlit as st
import os
import time
import itertools
from concurrent.futures import ThreadPoolExecutor
from crew import run_crew
from tools.pdf_tool import generate_pdf_manual


st.set_page_config(page_title="HALIMOZ AI", layout="wide")
st.title("HALIMOZ AI")


loading_texts = [
    "Halimoz is analyzing the video...",
    "Extracting key insights...",
    "Processing the script...",
    "Generating the summary...",
    "Identifying core ideas and explanations...",
    "Almost done, please wait..."
]

# for user input
video_url = st.text_input("Enter YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")
include_script = st.checkbox(" Show full video script")


st.markdown("""
<style>
div.stButton > button {
    height: 55px;
    font-size: 20px;
    border-radius: 12px;
}
</style>
""", unsafe_allow_html=True)
st.write("")

# for button alignment
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    # button placeholder to update text later
    btn_placeholder = st.empty()
    summarize = btn_placeholder.button("Summarize", use_container_width=True, key="main_btn")

st.markdown("---")

if summarize:
    if not video_url:
        st.warning("Please enter a URL first")
    else:
        btn_placeholder.button("Processing...", disabled=True, use_container_width=True, key="processing_btn")
        status_text = st.empty()
        
        try:
            # for running the crew in a separate thread
            with ThreadPoolExecutor() as executor:
                future = executor.submit(run_crew, video_url)
                
                # for loading animation
                for msg in itertools.cycle(loading_texts):
                    status_text.markdown(f"<h3 style='text-align: center; color: #9DB4C9;'> {msg}</h3>", unsafe_allow_html=True)
                    time.sleep(4.5)
                    if future.done():
                        break
                result = future.result()
            
            # delete loading text
            status_text.empty()


            # --- The Result ---
            summary_text = result["summary"]
            script_raw = result["script"]

            script_text = ""
            if hasattr(result, 'tasks_output') and len(result.tasks_output) > 0:
                script_text = result.tasks_output[0].raw

            if not script_text:
                script_text = script_raw
            
            # for showing full script if checkbox is selected
            if include_script and script_text:
                with st.expander("Full Video Script"):
                    display_script = script_text.replace(". ", ".\n\n")
                    st.text_area("Script Content", display_script, height=400)

            # for showing summary
            if summary_text:
                # for styled title
                st.markdown("<h1 style='text-align: center; color: #2E86C1; font-size: 32px;'>Analysis Summary</h1>", unsafe_allow_html=True)
                
                formatted_text = summary_text
                
                # for styled the summary
                sections = {
                    "Title": "Title",
                    "Overview": "Overview",
                    "Main Sections": "Main Sections",
                    "Key Takeaways": "Key Takeaways",
                    "Conclusion": "Conclusion"
                }
                for md_tag, label in sections.items():
                    html_replacement = f"<div style='font-size: 26px; color: #9DB4C9; font-weight: bold; margin-top: 25px; margin-bottom: 10px; border-bottom: 1px solid #eee;'>{label}</div>"
                    formatted_text = formatted_text.replace(f"{md_tag}\n*", f"{html_replacement}•&nbsp;")
                    formatted_text = formatted_text.replace(f"{md_tag}\n *", f"{html_replacement}•&nbsp;")
                    formatted_text = formatted_text.replace(md_tag, html_replacement)                
                formatted_text = formatted_text.replace(" * ", "<br>•&nbsp;")
                formatted_text = formatted_text.replace("\n*", "<br>•&nbsp;")

                # finally display the summary
                st.markdown(formatted_text, unsafe_allow_html=True)
            

            # PDF Download Section
            st.markdown("---")
            if include_script:
              # for script inclusion in PDF
               pdf_path = generate_pdf_manual(summary_text, script_raw)
            else:
               # without script inclusion in PDF
               pdf_path = generate_pdf_manual(summary_text, None)

            if os.path.exists(pdf_path):
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        label="Download Summary PDF",
                        data=f,
                        file_name="halimoz_summary.pdf",
                        mime="application/pdf"
                    )

            btn_placeholder.button("Summarize", use_container_width=True)
        except Exception as e:
            status_text.empty()
            btn_placeholder.button("Summarize", use_container_width=True)
            st.error(f"An error occurred: {str(e)}")

st.caption("Powered by HALIMOZ AI © 2026")