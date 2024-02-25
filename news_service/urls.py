from django.urls import path
from . import views

app_name = 'news_service'

urlpatterns = [
    path('', views.NewsListView.as_view(), name='news_list'),
    path('post/<slug:slug>', views.NewsDetailView.as_view(), name='news_detail'),
    path('create_news',
         views.CreateNewsView.as_view(), name='create_news'),
]
