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
        label='مشخصات شغل',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 10,
            'placeholder': 'مشخصات شغل را در اینجا قرار دهید...'
        })
    )
