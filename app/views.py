from django.shortcuts import render
from .models import NewsPost

def home(request):
    trending_news = NewsPost.objects.order_by('-views', '-published_at')[:3]
    latest_news = NewsPost.objects.exclude(id__in=trending_news.values_list('id', flat=True)).order_by('-published_at')[:5]
    return render(request, 'home.html', {
        'trending_news': trending_news,
        'latest_news': latest_news,
    })

def about(request):
    return render(request, 'about.html')

def news_list(request):
    trending_news = NewsPost.objects.order_by('-views', '-published_at')[:5]  # Most reached
    latest_news = NewsPost.objects.order_by('-published_at')[:10]
    featured_news = NewsPost.objects.filter(views__gte=100).order_by('-views')[:3]  # Example threshold

    context = {
        'trending_news': trending_news,
        'latest_news': latest_news,
        'featured_news': featured_news,
    }

    news = NewsPost.objects.order_by('-published_at')
    return render(request, 'news_list.html', context)