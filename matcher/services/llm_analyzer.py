from huggingface_hub import InferenceClient
import os
import logging

logger = logging.getLogger(__name__)


def analyze_resume(resume_text: str, jd_text: str):
    messages = [
        {
            "role": "system",
            "content": "/no_think\nشما یک تحلیلگر منابع انسانی هستید. فقط JSON خروجی بدهید."
        },
        {
            "role": "user",
            "content": f"""رزومه زیر را با مشخصات شغل مقایسه کن.

=== رزومه ===
{resume_text}

=== مشخصات شغل ===
{jd_text}

=== قوانین ===
۱. matched_skills فقط شامل مهارت‌هایی باشد که هم در رزومه و هم در شغل وجود دارد.
۲. missing_skills شامل تمام نیازهای شغلی که در رزومه نیست — شامل مدرک، مهارت، تجربه.
۳. امتیاز = matched / (matched + missing) × ۱۰۰ گرد شده به ۵.
۴. متن‌ها فارسی. فقط نام ابزارها انگلیسی.

{{
  "match_score": <عدد>,
  "matched_skills": [<لیست>],
  "missing_skills": [<لیست>],
  "improvement_suggestions": [<۳-۵ پیشنهاد>],
  "interview_questions": [<۵-۸ سوال>],
  "summary": "<۲-۳ جمله>"
}}"""
        }
    ]

    token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
    if token == "your-token-here":
        token = None
    client = InferenceClient(token=token, timeout=50)

    model = "Qwen/Qwen3-8B"
    logger.info(f"Calling LLM model: {model}")
    result = client.chat_completion(
        messages=messages,
        model=model,
        max_tokens=2048,
        temperature=0.1,
        top_p=0.9
    )
    choice = result.choices[0]
    content = choice.message.content
    if not content:
        content = getattr(choice.message, 'reasoning_content', None) or ""
    return content
