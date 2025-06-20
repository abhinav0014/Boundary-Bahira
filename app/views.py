from django.shortcuts import render
from .models import NewsPost

def home(request):
    latest_news = NewsPost.objects.order_by('-published_at')[:5]
    return render(request, 'home.html', {'latest_news': latest_news})

def about(request):
    return render(request, 'about.html')

def news_list(request):
    news = NewsPost.objects.order_by('-published_at')
    return render(request, 'news_list.html', {'news': news})