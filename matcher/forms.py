from django import forms

class ResumeAnalysisForm(forms.Form):
    resume_file = forms.FileField(
        label='فایل رزومه (PDF)',
        widget=forms.ClearableFileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf'
        })
    )
    job_description = forms.CharField(
        label='Job Description',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 10,
            'placeholder': 'Job Description را اینجا paste کنید...'
        })
    )
