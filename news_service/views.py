from typing import Any
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views import generic
from . import models
from . import forms
from django.contrib.auth import get_user_model
User = get_user_model()  # nopep8


# Create your views here.
# VISTAS RELACIONADAS CON NEWS

class ThemeCreateView(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'news_service.add_theme'
    permission_denied_message = "Sorry, you don't have the permission to access"
    form_class = forms.AddThemeForm
    template_name = 'news_service/add_theme.html'

    def get_success_url(self):
        user = models.Journalist.objects.get(user=self.request.user)
        return reverse_lazy('accounts:board', kwargs={'slug': user.slug})


class NewsListView(generic.ListView):
    model = models.Post
    template_name = 'news_service/news_list.html'


class NewsDetailView(generic.DetailView):
    model = models.Post
    template_name = 'news_service/news_detail.html'


class CreateNewsView(LoginRequiredMixin, generic.CreateView):
    model = models.Post
    form_class = forms.NewsCreateForm
    template_name = 'news_service/create_news.html'
    success_url = "news_service/news_list.html"

    def form_valid(self, form):
        form.instance.main_author = self.request.user.journalist
        return super().form_valid(form)


# VISTAS RELACIONADAS CON JOURNALISTS
