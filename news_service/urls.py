from django.urls import path
from . import views

app_name = 'news_service'

urlpatterns = [
    path('', views.NewsListView.as_view(), name='news_list'),
    path('post/<slug:slug>', views.NewsDetailView.as_view(), name='news_detail'),
    path('board/<slug:slug>', views.BoardView.as_view(), name='board'),
    path('create_news',
         views.CreateNewsView.as_view(), name='create_news'),
    path('journalists', views.JournalistsList.as_view(), name='journalists_list')
]
