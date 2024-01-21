from typing import Any
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse
from django.views import generic
from . import models

# Create your views here.


class NewsListView(generic.ListView):
    model = models.Post
    template_name = 'news_service/news_list.html'


class NewsDetailView(generic.DetailView):
    model = models.Post
    template_name = 'news_service/news_detail.html'


class BoardView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'news_service/board.html'
