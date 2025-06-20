from django.contrib import admin
from django.urls import path
from .views import *
from django.contrib.sitemaps.views import sitemap
from .sitemaps import StaticViewSitemap

sitemaps = {
    'static': StaticViewSitemap,
}
    
urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('news/', news_list, name='news'),
    path('sitemap', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]
