from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import NewsPost, NewsPostImage
from .forms import NewsPostForm, NewsPostImageForm
from django.utils import timezone

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
    
    def form_valid(self, form):
        response = super().form_valid(form)
        
        # Handle Facebook sharing if selected
        if form.cleaned_data.get('share_to_facebook'):
            post = form.instance
            
            # Determine what to include based on form data
            include_title = form.cleaned_data.get('include_title', True)
            include_excerpt = form.cleaned_data.get('include_excerpt', True)
            include_link = form.cleaned_data.get('include_link', True)
            
            post.post_to_facebook(
                include_title=include_title,
                include_excerpt=include_excerpt,
                include_link=include_link
            )
            
        return response

# Update view for news posts
class NewsPostUpdateView(LoginRequiredMixin, UpdateView):
    model = NewsPost
    form_class = NewsPostForm
    template_name = 'news_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_create'] = False
        return context
    
    def form_valid(self, form):
        # Check if this is a Facebook share-only request
        if 'share_only' in self.request.POST:
            post = form.instance
            post.post_to_facebook()
            return redirect('news_detail', pk=post.pk)
            
        response = super().form_valid(form)
        
        # Handle Facebook sharing if selected
        if form.cleaned_data.get('share_to_facebook'):
            post = form.instance
            
            # Determine what to include based on form data
            include_title = form.cleaned_data.get('include_title', True)
            include_excerpt = form.cleaned_data.get('include_excerpt', True)
            include_link = form.cleaned_data.get('include_link', True)
            
            post.post_to_facebook(
                include_title=include_title,
                include_excerpt=include_excerpt,
                include_link=include_link
            )
            
        return response

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
            
            # Handle Facebook sharing if selected
            if form.cleaned_data.get('share_to_facebook'):
                # Get post style and options
                post_style = form.cleaned_data.get('post_style', 'full')
                include_title = form.cleaned_data.get('include_title', True)
                include_excerpt = form.cleaned_data.get('include_excerpt', True)
                include_image = form.cleaned_data.get('include_image', True)
                include_link = form.cleaned_data.get('include_link', True)
                
                # Post to Facebook with the selected options
                news_post.post_to_facebook(
                    post_type=post_style,
                    include_title=include_title,
                    include_excerpt=include_excerpt,
                    include_image=include_image and bool(image),  # Only if we have an image
                    include_link=include_link,
                    image=image if include_image else None
                )
                
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
    # Basic stats
    recent_posts = NewsPost.objects.order_by('-published_at')[:10]
    total_posts = NewsPost.objects.count()
    total_views = NewsPost.objects.aggregate(total=Sum('views'))['total'] or 0
    total_images = NewsPostImage.objects.count()
    
    # Enhanced stats
    posts_this_month = NewsPost.objects.filter(
        published_at__month=timezone.now().month,
        published_at__year=timezone.now().year
    ).count()
    
    # Most viewed articles
    most_viewed = NewsPost.objects.order_by('-views')[:5]
    
    # Category distribution
    category_counts = {}
    for category_choice in NewsPost.CATEGORY_CHOICES:
        code, name = category_choice
        count = NewsPost.objects.filter(category=code).count()
        category_counts[name] = count
    
    # Articles with no images
    posts_without_images = NewsPost.objects.filter(images__isnull=True).count()
    
    # User activity if you're tracking that
    if request.user.is_superuser:
        # Only show this to superusers
        recent_users = User.objects.filter(
            last_login__isnull=False
        ).order_by('-last_login')[:5]
    else:
        recent_users = None
    
    stats = {
        'total_posts': total_posts,
        'total_views': total_views,
        'total_images': total_images,
        'posts_this_month': posts_this_month,
        'avg_views_per_post': round(total_views / total_posts if total_posts > 0 else 0, 1),
        'posts_without_images': posts_without_images,
        'category_distribution': category_counts
    }
    
    return render(request, 'dashboard.html', {
        'recent_posts': recent_posts,
        'most_viewed_posts': most_viewed,
        'recent_users': recent_users,
        'stats': stats,
    })