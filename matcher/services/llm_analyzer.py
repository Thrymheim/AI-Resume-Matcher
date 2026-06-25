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

=== قوانین سخت‌گیرانه ===
۱. matched_skills فقط شامل مهارت‌هایی باشد که هم در رزومه وجود دارد و هم مشخصاً در مشخصات شغل خواسته شده. اگر رزومه Python دارد ولی شغل Python نخواسته، Python نباید در matched باشد.
۲. missing_skills شامل تمام نیازهای شغلی باشد که در رزومه وجود ندارد — شامل مدرک تحصیلی، مهارت‌ها، تجربه، و ابزارها.
۳. اگر شغل PhD خواسته و رزومه Bachelor دارد، این یک missing skill مهم است.
۴. امتیاز = تعداد matched / (تعداد matched + تعداد missing) × ۱۰۰، گرد شده به ۵
۵. تمام متن‌ها فارسی. فقط نام ابزارها انگلیسی.

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
