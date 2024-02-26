from django.urls import path
from . import views

app_name = 'news_service'

urlpatterns = [
    path('', views.NewsListView.as_view(), name='news_list'),
    path('post/<slug:slug>', views.NewsDetailView.as_view(), name='news_detail'),
    path('add_theme', views.ThemeCreateView.as_view(), name='add_theme'),
    path('create_news',
         views.CreateNewsView.as_view(), name='create_news'),
]
