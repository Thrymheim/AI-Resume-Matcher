from huggingface_hub import InferenceClient
import os
import logging

logger = logging.getLogger(__name__)


def analyze_resume(resume_text: str, jd_text: str):
    messages = [
        {
            "role": "system",
            "content": "/no_think\nشما یک تحلیلگر سخت‌گیر منابع انسانی هستید. فقط JSON خروجی بدهید. فکر نکنید."
        },
        {
            "role": "user",
            "content": f"""مقایسه کن. فقط JSON بده. بدون فکر کردن.

=== رزومه ===
{resume_text}

=== شغل ===
{jd_text}

قوانین:
- فقط مهارت‌هایی که صراحتاً در رزومه ذکر شده matched باشند
- امتیاز = matched / (matched + missing) × ۱۰۰، گرد شده به ۵
- تمام متن‌ها به فارسی. فقط نام ابزارها انگلیسی

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
