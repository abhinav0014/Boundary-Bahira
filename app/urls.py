from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap
from django.contrib.auth import views as auth_views

sitemaps = {
    'static': StaticViewSitemap,
}
    
urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('news/', views.NewsPostListView.as_view(), name='news_list'),
    path('news/<int:pk>/', views.NewsPostDetailView.as_view(), name='news_detail'),
    path('news/new/', views.NewsPostCreateView.as_view(), name='news_create'),
    path('news/<int:pk>/edit/', views.NewsPostUpdateView.as_view(), name='news_update'),
    path('news/<int:pk>/delete/', views.NewsPostDeleteView.as_view(), name='news_delete'),
    path('news/<int:pk>/add_image/', views.add_image_to_news, name='add_image'),
    path('sitemap', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
    
    # Admin login URLs
    path('admin/login/', auth_views.LoginView.as_view(template_name='admin/login.html'), name='admin_login'),
    path('admin/logout/', auth_views.LogoutView.as_view(next_page='home', http_method_names=['get', 'post']), name='admin_logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Password reset URLs
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='admin/password_reset.html',
             email_template_name='admin/password_reset_email.html',
             subject_template_name='admin/password_reset_subject.txt'
         ), 
         name='password_reset'),
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='admin/password_reset_done.html'
         ), 
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='admin/password_reset_confirm.html'
         ), 
         name='password_reset_confirm'),
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='admin/password_reset_complete.html'
         ), 
         name='password_reset_complete'),
]
