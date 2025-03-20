from django import forms
from .models import File
from django.core.exceptions import ValidationError

class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['name', 'file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            if file.size > 10 * 1024 * 1024:
                raise ValidationError("File size must be under 10MB")
            if not file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.svg')):
                raise ValidationError("Only image files (png, jpg, jpeg, svg) are allowed")
        return file