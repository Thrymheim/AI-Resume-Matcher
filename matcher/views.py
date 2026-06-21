import json
import os
import uuid
import re
import logging

from django.shortcuts import render
from django.conf import settings

from .forms import ResumeAnalysisForm
from .services.pdf_extractor import extract_text_from_pdf
from .services.text_chunker import chunk_text
from .services.vector_store import add_documents, similarity_search, clear_collection
from .services.llm_analyzer import analyze_resume

logger = logging.getLogger(__name__)


def index(request):
    form = ResumeAnalysisForm()
    return render(request, 'matcher/index.html', {'form': form})


def analyze(request):
    if request.method != 'POST':
        return render(request, 'matcher/index.html', {'form': ResumeAnalysisForm()})

    form = ResumeAnalysisForm(request.POST, request.FILES)
    if not form.is_valid():
        return render(request, 'matcher/index.html', {'form': form})

    resume_file = request.FILES['resume_file']
    job_description = form.cleaned_data['job_description']

    if not resume_file.name.endswith('.pdf'):
        form.add_error('resume_file', 'فایل باید PDF باشد')
        return render(request, 'matcher/index.html', {'form': form})

    session_id = str(uuid.uuid4())[:8]

    try:
        temp_dir = os.path.join(settings.MEDIA_ROOT, 'temp')
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, f"{session_id}_{resume_file.name}")

        with open(temp_path, 'wb+') as f:
            for chunk in resume_file.chunks():
                f.write(chunk)
        logger.info(f"Resume saved to {temp_path}")

        resume_text = extract_text_from_pdf(temp_path)
        os.remove(temp_path)
        logger.info(f"Extracted {len(resume_text)} chars from PDF")

        if not resume_text.strip():
            form.add_error('resume_file', 'متنی از رزومه استخراج نشد')
            return render(request, 'matcher/index.html', {'form': form})

        resume_chunks = chunk_text(resume_text)
        logger.info(f"Resume chunks: {len(resume_chunks)}")

        collection_name = f"analysis_{session_id}"
        clear_collection(collection_name)

        resume_metas = [{"source": "resume", "chunk_index": i} for i in range(len(resume_chunks))]
        add_documents(resume_chunks, collection_name, resume_metas)

        relevant_chunks = similarity_search(job_description, collection_name, k=10)
        relevant_texts = [doc.page_content for doc in relevant_chunks]
        logger.info(f"Found {len(relevant_chunks)} relevant resume chunks")

        logger.info("Calling LLM for analysis...")
        raw_result = analyze_resume(relevant_texts, job_description)
        logger.info(f"LLM response received, length: {len(raw_result)}")

        result = parse_llm_output(raw_result)

        clear_collection(collection_name)

        history_entry = {
            'resume_filename': resume_file.name,
            'match_score': result.get('match_score', 0),
            'matched_skills': result.get('matched_skills', []),
            'missing_skills': result.get('missing_skills', []),
            'improvement_suggestions': result.get('improvement_suggestions', []),
            'interview_questions': result.get('interview_questions', []),
            'summary': result.get('summary', ''),
            'job_description': job_description[:200] + '...' if len(job_description) > 200 else job_description,
        }

        if 'analysis_history' not in request.session:
            request.session['analysis_history'] = []
        request.session['analysis_history'].insert(0, history_entry)
        request.session['analysis_history'] = request.session['analysis_history'][:20]
        request.session.modified = True

        context = {
            'result': result,
            'resume_filename': resume_file.name,
            'job_description': job_description,
        }
        return render(request, 'matcher/result.html', context)

    except Exception as e:
        logger.exception("Error during resume analysis")
        form.add_error(None, f'خطا در پردازش: {str(e)}')
        return render(request, 'matcher/index.html', {'form': form})


def parse_llm_output(raw: str) -> dict:
    try:
        json_match = re.search(r'\{[\s\S]*\}', raw)
        if json_match:
            return json.loads(json_match.group())
    except json.JSONDecodeError:
        pass

    return {
        'match_score': 0,
        'matched_skills': [],
        'missing_skills': [],
        'improvement_suggestions': [],
        'interview_questions': [],
        'summary': raw
    }


def history(request):
    results = request.session.get('analysis_history', [])
    return render(request, 'matcher/history.html', {'results': results})
