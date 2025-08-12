import streamlit as st
import streamlit.components.v1 as components
from utils.llm import generate_intro_and_questions, summarize_candidate
from utils.stt import transcribe_webm_with_whisper_local
from utils.tts import text_to_speech
import json
import os


st.set_page_config(page_title="AI Video Interview Bot", layout="centered")
st.title("🎤 AI-Powered Video Interview Bot")

# Step 1: Role Input
name=st.text_area("name")
role_title = st.text_input("Role Title")
role_description = st.text_area("Role Description")

if st.button("Start Interview"):
    with st.spinner("Generating questions..."):
        full_text = generate_intro_and_questions(role_title, role_description)
        lines = full_text.strip().split("\n")
        st.session_state.full_text = full_text 
        st.session_state.greeting = lines[0]
        text_to_speech(lines[0])
        st.session_state.questions = [q for q in lines[2:] if q.strip()]
        st.session_state.current_q = 0
        st.session_state.responses = []


# Step 2: Interview Flow
if "questions" in st.session_state:
    if st.session_state.current_q < len(st.session_state.questions):
        st.subheader(f"❓ Question {st.session_state.current_q + 1}")
        st.markdown(st.session_state.questions[st.session_state.current_q])
        st.markdown("Record your response below and download it before continuing.")
        components.html(open("/Users/gauravjangid/Desktop/mvp/templates/recorder.html").read(), height=600)

        if st.button("Next Question"):
            st.session_state.current_q += 1
    else:
        st.success("✅ Interview complete!")
        st.markdown("Upload your recorded responses for transcription and evaluation.")

        uploaded_files = st.file_uploader("Upload your video responses", accept_multiple_files=True)

        if uploaded_files and st.button("Generate Summary"):
            transcripts = []
            for file in uploaded_files:
                st.write(f"Transcribing {file.name}...")
                text = transcribe_webm_with_whisper_local(file)
                transcripts.append(f"{file.name}: {text}")
            
            full_transcript = "\n".join(transcripts)
            summary = summarize_candidate(name,full_transcript, role_title,st.session_state.full_text )
        
       

        # After displaying the summary
            if summary:
                candidate_data = {
                    "name": name,
                    "role": role_title,
                    "transcript": full_transcript,
                    "summary": summary
                }

                os.makedirs("data", exist_ok=True)
                submissions_path = "data/submissions.json"

                with open(submissions_path, "a") as f:
                    f.write(json.dumps(candidate_data) + "\n")

                st.success("✅ Candidate data saved successfully!")


st.markdown("---")
st.header("📋 Recruiter Dashboard")

# Optional: Filter by role
role_filter = st.text_input("Filter by Role Title")

submissions_path = "data/submissions.json"
if os.path.exists(submissions_path):
    with open(submissions_path) as f:
        lines = f.readlines()

    if not lines:
        st.info("No candidate submissions found.")
    else:
        for line in lines:
            try:
                data = json.loads(line)
                if role_filter and role_filter.lower() not in data["role"].lower():
                    continue

                st.subheader(f"🧑 {data['name']} — {data['role']}")
                st.markdown("**Summary:**")
                st.markdown(data["summary"])

                with st.expander("📄 View Transcript"):
                    st.markdown(data["transcript"])
            except Exception as e:
                st.error(f"Error loading submission: {e}")
else:
    st.warning("Submissions file not found.")
