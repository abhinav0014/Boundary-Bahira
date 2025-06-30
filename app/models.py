from django.db import models
from django.urls import reverse
from .utils import post_to_facebook
from django.contrib.sites.models import Site

class NewsPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    source_url = models.URLField(blank=True, null=True)
    views = models.PositiveIntegerField(default=0)  # Add this line

    CATEGORY_CHOICES = (
        ('nepal', 'Nepal Cricket'),
        ('associate', 'Associate Cricket'),
        ('icc', 'ICC Events'),
        ('other', 'Other'),
    )
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """Return the URL to access a detail record for this post."""
        return reverse('news_detail', args=[str(self.id)])

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            # Compose the message
            message = f"{self.title}\n\n{self.content[:200]}..."
            # Build the full URL (adjust domain as needed)
            domain = Site.objects.get_current().domain
            link = f"https://{domain}{self.get_absolute_url()}"
            post_to_facebook(message, link)

    def post_to_facebook(self, post_type='full', include_title=True, include_excerpt=True, 
                    include_image=True, include_link=True, image=None):
        """
        Post this news article to Facebook with the specified options
        """
        from .utils import post_to_facebook as fb_post
        success, result = fb_post(
            post=self,
            post_type=post_type,
            include_title=include_title,
            include_excerpt=include_excerpt,
            include_image=include_image,
            include_link=include_link,
            image=image
        )
        
        # Optional: store the result or post ID for future reference
        if success:
            # You could save the Facebook post ID to track it
            facebook_post_id = result.get('id')
            # self.facebook_post_id = facebook_post_id  # If you add this field to your model
            # self.save(update_fields=['facebook_post_id'])
            pass
            
        return success

class NewsPostImage(models.Model):
    news_post = models.ForeignKey(NewsPost, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='news_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)