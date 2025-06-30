from django import forms
from .models import NewsPost, NewsPostImage

class NewsPostForm(forms.ModelForm):
    class Meta:
        model = NewsPost
        fields = ['title', 'content', 'source_url', 'category']
        
    # Add hidden fields for Facebook sharing options
    share_to_facebook = forms.BooleanField(required=False, initial=False)
    include_title = forms.BooleanField(required=False, initial=True)
    include_excerpt = forms.BooleanField(required=False, initial=True)
    include_link = forms.BooleanField(required=False, initial=True)

class NewsPostImageForm(forms.ModelForm):
    class Meta:
        model = NewsPostImage
        fields = ['image']
        
    # Add fields for Facebook sharing options
    share_to_facebook = forms.BooleanField(required=False, initial=False)
    post_style = forms.ChoiceField(
        choices=[('full', 'Full Post'), ('image', 'Image Only'), ('link', 'Link Post')],
        required=False,
        initial='full'
    )
    include_title = forms.BooleanField(required=False, initial=True)
    include_excerpt = forms.BooleanField(required=False, initial=True)
    include_image = forms.BooleanField(required=False, initial=True)
    include_link = forms.BooleanField(required=False, initial=True)