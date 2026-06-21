from django.contrib import admin
from .models import AnalysisResult

@admin.register(AnalysisResult)
class AnalysisResultAdmin(admin.ModelAdmin):
    list_display = ['resume_filename', 'match_score', 'created_at']
    list_filter = ['created_at']
    search_fields = ['resume_filename']
