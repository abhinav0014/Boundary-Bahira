from django.db import models
from django.urls import reverse
from .utils import post_to_facebook

class NewsPost(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    source_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news_list') + f"#post-{self.id}"

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)
        if is_new:
            # Compose the message
            message = f"{self.title}\n\n{self.content[:200]}..."
            # Build the full URL (adjust domain as needed)
            from django.contrib.sites.models import Site
            domain = Site.objects.get_current().domain
            link = f"https://{domain}{self.get_absolute_url()}"
            post_to_facebook(message, link)

class NewsPostImage(models.Model):
    news_post = models.ForeignKey(NewsPost, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='news_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)