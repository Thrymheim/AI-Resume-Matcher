from django.db import models

class AnalysisResult(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    resume_filename = models.CharField(max_length=255)
    job_description = models.TextField()
    match_score = models.FloatField()
    matched_skills = models.JSONField(default=list)
    missing_skills = models.JSONField(default=list)
    improvement_suggestions = models.JSONField(default=list)
    interview_questions = models.JSONField(default=list)
    full_analysis = models.TextField()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.resume_filename} - {self.match_score}%"
