from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import NewsPost, NewsPostImage
from .forms import NewsPostForm, NewsPostImageForm

# List view for news posts
class NewsPostListView(ListView):
    model = NewsPost
    template_name = 'news_list.html'
    context_object_name = 'news_posts'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = NewsPost.objects.all().order_by('-published_at')
        
        # Get category filter from URL query parameter
        category = self.request.GET.get('category', None)
        if category:
            queryset = queryset.filter(category=category)
        
        # Handle sorting
        sort_by = self.request.GET.get('sort', None)
        if sort_by == 'popular':
            queryset = queryset.order_by('-views')
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Pass current filters to template for highlighting active button
        context['current_category'] = self.request.GET.get('category', 'all')
        context['current_sort'] = self.request.GET.get('sort', 'latest')
        
        # Get trending and featured news
        excluded_ids = [post.id for post in context['news_posts']]
        
        # Get trending news (most viewed)
        context['trending_news'] = NewsPost.objects.exclude(
            id__in=excluded_ids
        ).order_by('-views', '-published_at')[:5]
        
        # Get featured news (posts with views above a threshold)
        context['featured_news'] = NewsPost.objects.filter(
            views__gte=10
        ).exclude(
            id__in=excluded_ids
        ).order_by('-published_at')[:3]
        
        return context

# Detail view for a specific news post
class NewsPostDetailView(DetailView):
    model = NewsPost
    template_name = 'news_detail.html'
    context_object_name = 'news_post'
    
    def get_object(self):
        # Get the object and increment the view count
        obj = super().get_object()
        obj.views += 1
        obj.save()
        return obj

# Create view for news posts
class NewsPostCreateView(LoginRequiredMixin, CreateView):
    model = NewsPost
    form_class = NewsPostForm
    template_name = 'news_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_create'] = True
        return context

# Update view for news posts
class NewsPostUpdateView(LoginRequiredMixin, UpdateView):
    model = NewsPost
    form_class = NewsPostForm
    template_name = 'news_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_create'] = False
        return context

# Delete view for news posts
class NewsPostDeleteView(LoginRequiredMixin, DeleteView):
    model = NewsPost
    template_name = 'news_confirm_delete.html'
    success_url = reverse_lazy('news_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Ensure news_post is in the context
        context['news_post'] = self.get_object()
        return context
    
    def get_success_url(self):
        return reverse('news_list')  # Always redirect to the news list after deletion
    
    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except Exception:
            # If anything goes wrong during deletion, redirect to list view
            return redirect('news_list')

# Image upload view
def add_image_to_news(request, pk):
    news_post = get_object_or_404(NewsPost, pk=pk)
    
    if request.method == 'POST':
        form = NewsPostImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.save(commit=False)
            image.news_post = news_post
            image.save()
            return redirect('news_detail', pk=news_post.pk)
    else:
        form = NewsPostImageForm()
    
    return render(request, 'add_image.html', {
        'form': form,
        'news_post': news_post
    })

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

# Add this view
@login_required
def dashboard(request):
    recent_posts = NewsPost.objects.order_by('-published_at')[:10]
    
    stats = {
        'total_posts': NewsPost.objects.count(),
        'total_views': NewsPost.objects.aggregate(total=Sum('views'))['total'] or 0,
        'total_images': NewsPostImage.objects.count(),
    }
    
    return render(request, 'dashboard.html', {
        'recent_posts': recent_posts,
        'stats': stats,
    })