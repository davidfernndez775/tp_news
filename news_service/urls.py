from django.urls import path
from . import views

app_name = 'news_service'

urlpatterns = [
    path('', views.NewsListView.as_view(), name='news_list'),
    path('post/<slug:slug>', views.NewsDetailView.as_view(), name='news_detail'),
    path('add_theme', views.ThemeCreateView.as_view(), name='add_theme'),
    path('create_news',
         views.CreateNewsView.as_view(), name='create_news'),
    path('unapprove_news', views.UnapproveNewsListView.as_view(),
         name='unapprove_news'),
    path('post/<int:pk>/approve/', views.approve_post, name='approve_post'),
    path('post/<int:pk>/hide/', views.hide_post, name='hide_post'),
    path('politics', views.PoliticsListView.as_view(), name='politics'),
    path('economics', views.EconomicsListView.as_view(), name='economics'),
    path('sports', views.SportsListViews.as_view(), name='sports'),
    path('create_comment', views.CreateCommentView.as_view(), name='create_comment'),
]
