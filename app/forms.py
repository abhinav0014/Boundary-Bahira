from django import forms
from .models import NewsPost, NewsPostImage

class NewsPostForm(forms.ModelForm):
    class Meta:
        model = NewsPost
        fields = ['title', 'content', 'source_url']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10}),
        }

class NewsPostImageForm(forms.ModelForm):
    class Meta:
        model = NewsPostImage
        fields = ['image']