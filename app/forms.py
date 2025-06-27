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
    POST_STYLE_CHOICES = [
        ("full", "Article + Images + Link"),
        ("image_caption", "Image(s) with Title as Caption"),
        ("link", "Only Link"),
    ]
    post_style = forms.ChoiceField(choices=POST_STYLE_CHOICES, required=True, label="Facebook Post Style")

    class Meta:
        model = NewsPostImage
        fields = ['image']