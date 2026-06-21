from huggingface_hub import InferenceClient
import os
import logging

logger = logging.getLogger(__name__)


def analyze_resume(resume_chunks: list, jd_text: str):
    resume_context = "\n".join(resume_chunks)

    messages = [
        {
            "role": "system",
            "content": """You are a strict HR analyst. Your job is to compare a resume against a job description.

CRITICAL LANGUAGE RULE — ABSOLUTELY MANDATORY:
ALL your output MUST be in Persian (Farsi). EVERY sentence, EVERY suggestion, EVERY question, EVERY summary — in Farsi. The ONLY exception is tool/technology names like Python, Docker, Selenium, ISO 10816 which stay in English. NEVER write sentences in English. NEVER. Even if the resume and JD are in English, your analysis output must be in Farsi. This is a hard rule with zero exceptions.

RULES — follow exactly:
1. ONLY mark a skill as "matched" if the resume TEXT literally mentions it. Do NOT infer, assume, or guess.
2. Example: If the resume says "Python" but the JD requires "vibration analysis with Python", the resume does NOT have "vibration analysis" — only "Python".
3. Example: If the JD requires "Docker" and the resume never mentions Docker, it is MISSING.
4. If the resume is for an AI/NLP engineer and the JD is for a mechanical vibration analyst, the match score should be very low (10-30%).
5. Every matched skill must have a direct quote or reference from the resume as proof.
6. Respond with valid JSON only. No markdown code blocks."""
        },
        {
            "role": "user",
            "content": f"""Compare this resume against this job description.

=== FULL RESUME TEXT ===
{resume_context}

=== JOB DESCRIPTION ===
{jd_text}

=== INSTRUCTIONS ===
Step 1: List EVERY skill/requirement from the JD.
Step 2: For each one, check if the resume EXPLICITLY mentions it. Quote the exact text if yes.
Step 3: Only include in "matched_skills" items where you found EXACT evidence in the resume text above.
Step 4: Everything else goes into "missing_skills".
Step 5: Calculate match_score = (matched / total JD requirements) * 100, rounded to nearest 5.

REMINDER: ALL output values MUST be in Persian (Farsi). Tool/technology names stay in English. NEVER write sentences in English.

Respond with ONLY this JSON:
{{
  "match_score": <number 0-100>,
  "matched_skills": [<only skills with EXACT evidence from resume text above>],
  "missing_skills": [<all JD requirements with no evidence in resume — in Persian>],
  "improvement_suggestions": [<3-5 specific suggestions in Persian>],
  "interview_questions": [<5-8 questions in Persian>],
  "summary": "<2-3 sentence honest assessment in Persian>"
}}"""
        }
    ]

    token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if token == "your-token-here":
        token = None
    client = InferenceClient(token=token)

    model = "Qwen/Qwen3-8B"
    logger.info(f"Calling LLM model: {model}")
    result = client.chat_completion(
        messages=messages,
        model=model,
        max_tokens=4096,
        temperature=0.1,
        top_p=0.9
    )
    choice = result.choices[0]
    content = choice.message.content
    if not content:
        content = getattr(choice.message, 'reasoning_content', None) or ""
    return content
