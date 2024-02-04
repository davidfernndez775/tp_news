from typing import Any
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views import generic
from . import models
from . import forms
from django.contrib.auth import get_user_model
User = get_user_model()  # nopep8


# Create your views here.


class NewsListView(generic.ListView):
    model = models.Post
    template_name = 'news_service/news_list.html'


class NewsDetailView(generic.DetailView):
    model = models.Post
    template_name = 'news_service/news_detail.html'


class BoardView(LoginRequiredMixin, generic.DetailView):
    model = models.Journalist
    template_name = 'news_service/board.html'


class CreateNewsView(LoginRequiredMixin, generic.CreateView):
    model = models.Post
    form_class = forms.NewsCreateForm
    template_name = 'news_service/create_news.html'
    success_url = "//"


class JournalistsList(generic.ListView):
    model = models.Journalist
    template_name = 'news_service/journalists.html'
