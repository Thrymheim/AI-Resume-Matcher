from huggingface_hub import InferenceClient
import os
import logging

logger = logging.getLogger(__name__)


def analyze_resume(resume_text: str, jd_text: str):
    messages = [
        {
            "role": "system",
            "content": "/no_think\nشما یک تحلیلگر سخت‌گیر منابع انسانی هستید. فقط JSON خروجی بدهید."
        },
        {
            "role": "user",
            "content": f"""رزومه زیر را با مشخصات شغل مقایسه کن.

=== رزومه ===
{resume_text}

=== مشخصات شغل ===
{jd_text}

=== قوانین بسیار سخت‌گیرانه ===
۱. matched_skills فقط شامل مهارت‌هایی باشد که صراحتاً در مشخصات شغل خواسته شده و دقیقاً در رزومه وجود دارد. اگر شغل Django نخواسته، Django نباید در matched باشد حتی اگر رزومه Django داشته باشد.
۲. اگر شغل Python خواسته و رزومه Python دارد، فقط بنویس Python. نه Django، نه Flask، نه چیز دیگری.
۳. missing_skills شامل تمام نیازهای شغلی باشد — مدرک، مهارت، ابزار، تجربه.
۴. اگر رزومه Bachelor و شغل PhD خواسته، PhD در missing باشد.
۵. امتیاز = matched / (matched + missing) × ۱۰۰ گرد شده به ۵.
۶. متن‌ها فارسی. فقط نام ابزارها انگلیسی.

{{
  "match_score": <عدد>,
  "matched_skills": [<فقط مهارت‌هایی که در هر دو رزومه و شغل وجود دارند>],
  "missing_skills": [<تمام نیازهای شغلی که در رزومه نیست>],
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
