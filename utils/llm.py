# utils/llm.py
import os,re
import json
from typing import Dict, Any
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash",
    temperature=0.7,
    max_output_tokens=512  # note: updated param name in latest versions
)

    
def generate_intro_and_questions(role_title: str, role_description: str, n_questions: int = 6) -> Dict:
    prompt = f"""
    You're an AI interviewer. Greet the candidate and generate 5 interview questions for the role: {role_title}.
    Role Description: {role_description}
    you can generate only 6 things one is greet and in next line you have to start generate question
    """
    resp = llm.invoke(prompt)
    return resp.content


import json
from typing import Dict, Any

def summarize_candidate(name:str,role_title: str, transcript: str, interview_questions: str) -> Dict[str, Any]:
    skills = ["Communication", "Technical Knowledge", "Problem Solving", "Confidence", "Teamwork"]

    prompt = f"""
    You're an AI recruiter evaluating a candidate name {name} for the role of **{role_title}**.
    
    Below are the interview questions and the candidate's transcripted responses.

    Interview Questions:
    {interview_questions}

    Candidate Responses:
    {transcript}

    Please analyze and return a structured JSON with the following keys:
    - name
    - strengths: List of strengths
    - weaknesses: List of weaknesses
    - skills_assessment: Dictionary with these skill scores (1–10): {', '.join(skills)}
    - final_summary: A short paragraph summarizing the candidate's performance and fit for the role
    """

    response = llm.invoke(prompt)
    raw_output = response.content.strip()

    # Remove markdown-style code block formatting
    cleaned_output = re.sub(r"^```json|```$", "", raw_output, flags=re.MULTILINE).strip()

    try:
        result = json.loads(cleaned_output)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM response could not be parsed as JSON.\nRaw output:\n{raw_output}\n\nError: {e}")

    return result