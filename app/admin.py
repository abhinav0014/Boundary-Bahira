from django.contrib import admin
from .models import NewsPost, NewsPostImage

class NewsPostImageInline(admin.TabularInline):
    model = NewsPostImage
    extra = 1

@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    inlines = [NewsPostImageInline]
