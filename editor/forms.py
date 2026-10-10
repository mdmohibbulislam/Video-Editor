from django import forms
from .models import Video


class VideoUploadForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = ['title', 'original_file']
        widgets = {
            'original_file': forms.FileInput(attrs={'accept': 'video/*'})
        }


class VideoEditForm(forms.ModelForm):
    """Edit title. Optionally replace the original video file."""
    class Meta:
        model = Video
        fields = ['title', 'original_file']
        widgets = {
            'original_file': forms.FileInput(attrs={'accept': 'video/*'}),
            'title': forms.TextInput(attrs={'placeholder': 'Video title'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['original_file'].required = False
        self.fields['original_file'].help_text = 'Leave empty to keep the current file.'