from huggingface_hub import InferenceClient
import os
import logging

logger = logging.getLogger(__name__)


def analyze_resume(resume_text: str, jd_text: str):
    messages = [
        {
            "role": "system",
            "content": """شما یک تحلیلگر سخت‌گیر منابع انسانی هستید. وظیفه شما مقایسه یک رزومه با یک آگهی شغلی است.

قوانین مطلق — حتماً رعایت کنید:
فقط مهارت‌هایی که متن رزومه صراحتاً ذکر کرده matched باشند. حدس نزنید، فرض نکنید، استنتاج نکنید.
اگر رزومه برای یک مهندس AI است و شغل برای تحلیل ارتعاشات صنعتی است، امتیاز باید خیلی کم باشد (۱۰-۳۰٪).
تمام خروجی‌ها باید به زبان فارسی باشند. فقط نام ابزارها و فناوری‌ها مانند Python، Docker به انگلیسی بماند.
فقط با JSON معتبر پاسخ دهید. بدون markdown."""
        },
        {
            "role": "user",
            "content": f"""این رزومه را با مشخصات شغل مقایسه کنید.

=== متن کامل رزومه ===
{resume_text}

=== مشخصات شغل ===
{jd_text}

=== دستورالعمل‌ها ===
مرحله ۱: هر مهارت/نیاز شغلی را لیست کنید.
مرحله ۲: بررسی کنید آیا رزومه آن را صراحتاً ذکر کرده.
مرحله ۳: فقط مواردی که دقیقاً در رزومه وجود دارد در matched_skills قرار دهید.
مرحله ۴: بقیه در missing_skills قرار می‌گیرند.
مرحله ۵: فرمول امتیاز — حتماً دقیقاً از این فرمول استفاده کنید:
  match_score = (تعداد matched_skills) / (تعداد matched_skills + تعداد missing_skills) × ۱۰۰
  گرد کنید به نزدیک‌ترین ۵. از هیچ فرمول دیگری استفاده نکنید.
  مثال: ۲۱ matched + ۳ missing = ۲۱/(۲۱+۳)×۱۰۰ = ۸۷.۵ → گرد شود به ۸۵ یا ۹۰.

پاسخ فقط با این JSON باشد. تمام مقادیر متنی به فارسی باشند:
{{
  "match_score": <عدد ۰ تا ۱۰۰>,
  "matched_skills": [<فقط مهارت‌هایی که دقیقاً در رزومه وجود دارند>],
  "missing_skills": [<تمام نیازهای شغلی که در رزومه وجود ندارند — به فارسی>],
  "improvement_suggestions": [<۳ تا ۵ پیشنهاد خاص به فارسی>],
  "interview_questions": [<۵ تا ۸ سوال مصاحبه به فارسی>],
  "summary": "<ارزیابی صادقانه ۲ تا ۳ جمله‌ای به فارسی>"
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
