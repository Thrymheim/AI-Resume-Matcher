# AI Resume Matcher (تحلیلگر هوشمند رزومه)

ابزار هوشمند تحلیل رزومه که با استفاده از هوش مصنوعی، رزومه شما را با مشخصات شغل مقایسه کرده و گزارش دقیقی از مهارت‌ها، نقاط ضعف و پیشنهادات بهبود ارائه می‌دهد.

## امکانات

- **آپلود رزومه PDF** - استخراج و تحلیل متن از فایل‌های PDF
- **تطبیق مهارت‌ها** - مقایسه مهارت‌های رزومه با نیازهای شغل
- **تحلیل شکاف‌ها** - شناسایی مهارت‌های مفقود و حوزه‌های ضعف
- **پیشنهادات بهبود** - راهکارهای عملی برای تقویت رزومه
- **سوالات مصاحبه** - تولید سوالات مرتبط بر اساس مشخصات شغل
- **امتیاز تطابق** - سنجش دقیق میزان هماهنگی رزومه با شغل (محاسبه خودکار بر اساس نسبت مهارت‌ها)
- **تاریخچه مبتنی بر نشست** - تاریخچه تحلیل هر کاربر فقط در مرورگر خودش ذخیره می‌شود
- **خروجی به زبان فارسی** - تمام نتایج تحلیل به زبان فارسی ارائه می‌شود
- **رابط کاربری فارسی** - تمام متون و راهنماها به زبان فارسی

## فناوری‌های استفاده شده

- **بک‌اند**: Django 5.x
- **هوش مصنوعی**: Hugging Face Inference API (Qwen/Qwen3-8B) برای تحلیل رزومه
- **پردازش PDF**: PyMuPDF برای استخراج متن از فایل‌های PDF

## نحوه کار

1. **آپلود رزومه**: کاربر فایل PDF رزومه را آپلود می‌کند
2. **استخراج متن**: PyMuPDF متن فایل را استخراج می‌کند
3. **تحلیل هوش مصنوعی**: متن رزومه و مشخصات شغل مستقیماً به مدل Qwen3-8B ارسال می‌شود
4. **محاسبه امتیاز**: امتیاز تطابق بر اساس نسبت مهارت‌های موجود به مفقود محاسبه می‌شود
5. **تولید گزارش**: نتایج شامل امتیاز، تحلیل مهارت‌ها و پیشنهادات به زبان فارسی است

## نصب و راه‌اندازی

### پیش‌نیازها
- Python 3.10+
- توکن Hugging Face (رایگان از huggingface.co)

### مراحل نصب

1. کلون کردن مخزن:
```bash
git clone https://github.com/Thrymheim/AI-Resume-Matcher.git
cd AI-Resume-Matcher
```

2. ایجاد محیط مجازی:
```bash
python -m venv venv
source venv/bin/activate  # در ویندوز: venv\Scripts\activate
```

3. نصب وابستگی‌ها:
```bash
pip install -r requirements.txt
```

4. تنظیم متغیرهای محیطی:
```bash
cp .env.example .env
# فایل .env را ویرایش کنید و توکن Hugging Face را وارد کنید
```

5. اجرای مایگریشن‌ها:
```bash
python manage.py migrate
```

6. راه‌اندازی سرور:
```bash
python manage.py runserver
```

7. مرورگر را باز کنید: `http://127.0.0.1:8000`

## متغیرهای محیطی

| متغیر | توضیحات | مقدار پیش‌فرض |
|--------|---------|---------------|
| `SECRET_KEY` | کلید مخفی Django | در تولید الزامی |
| `DEBUG` | حالت اشکال‌زدایی | `True` |
| `ALLOWED_HOSTS` | میزبان‌های مجاز | `localhost,127.0.0.1` |
| `HUGGINGFACEHUB_API_TOKEN` | توکن API هوگینگ فیس | الزامی |
| `EMBEDDING_MODEL` | مدل تبدیل متن به بردار | `BAAI/bge-small-en-v1.5` |
| `LLM_MODEL` | مدل زبانی برای تحلیل | `Qwen/Qwen3-8B` |
| `CHUNK_SIZE` | اندازه هر بخش متن | `500` |
| `CHUNK_OVERLAP` | همپوشانی بین بخش‌ها | `50` |

## استقرار روی PythonAnywhere

1. کلون کردن پروژه و ایجاد محیط مجازی:
```bash
git clone https://github.com/Thrymheim/AI-Resume-Matcher.git
cd AI-Resume-Matcher
mkvirtualenv --python=/usr/bin/python3.12 venv
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
```

2. ایجاد فایل `.env`:
```bash
nano ~/AI-Resume-Matcher/.env
```
محتوا:
```
SECRET_KEY=your-random-secret-key
DEBUG=False
ALLOWED_HOSTS=yourusername.pythonanywhere.com
HUGGINGFACEHUB_API_TOKEN=hf_your_token_here
EMBEDDING_MODEL=BAAI/bge-small-en-v1.5
LLM_MODEL=Qwen/Qwen3-8B
CHUNK_SIZE=500
CHUNK_OVERLAP=50
```

3. از تب Web، مسیر WSGI را تنظیم کنید:
```python
import os, sys
project_home = '/home/yourusername/AI-Resume-Matcher'
if project_home not in sys.path:
    sys.path.append(project_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'ai_resume_matcher.settings'
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

4. Virtualenv را تنظیم کنید:
```
/home/yourusername/.virtualenvs/venv
```

5. Static files را تنظیم کنید:
- URL: `/static/`
- Directory: `/home/yourusername/AI-Resume-Matcher/staticfiles`

6. Reload کنید.

## استقرار با Docker

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py migrate
RUN python manage.py collectstatic --noinput
EXPOSE 8000
CMD ["gunicorn", "ai_resume_matcher.wsgi:application", "--bind", "0.0.0.0:8000"]
```

## حریم خصوصی

- تاریخچه تحلیل هر کاربر فقط در نشست مرورگر خودش ذخیره می‌شود
- هیچ داده‌ای بین کاربران به اشتراک گذاشته نمی‌شود
- فایل‌های رزومه بلافاصله پس از پردازش حذف می‌شوند
- هیچ ذخیره‌سازی دائمی از رزومه‌های کاربران انجام نمی‌شود

## مجوز

مجوز MIT - آزادانه از این پروژه استفاده و آن را تغییر دهید.

## سپاسگزاری

- [Hugging Face](https://huggingface.co) برای مدل‌های هوش مصنوعی
- [Django](https://www.djangoproject.com) برای فریمورک وب
- [PyMuPDF](https://pymupdf.readthedocs.io) برای پردازش PDF
