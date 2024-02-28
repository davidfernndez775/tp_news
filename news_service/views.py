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
from django.http import request
from django.shortcuts import redirect


# Create your views here.
# VISTAS RELACIONADAS CON POST

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

    def get_queryset(self):
        return models.Post.objects.filter(approve=True)


class UnapproveNewsListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'news_service.delete_post'
    permission_denied_message = "Sorry, you don't have the permission to access"
    model = models.Post
    template_name = 'news_service/unapprove_news.html'

    def get_queryset(self):
        return models.Post.objects.filter(approve=False)


class NewsDetailView(generic.DetailView):
    model = models.Post
    template_name = 'news_service/news_detail.html'


class CreateNewsView(LoginRequiredMixin, generic.CreateView):
    model = models.Post
    form_class = forms.NewsCreateForm
    template_name = 'news_service/create_news.html'
    success_url = "//"

    def get(self, request):
        form = forms.NewsCreateForm()
        return render(request, 'news_service/create_news.html', {'form': form})

    def post(self, request):
        form = forms.NewsCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.main_author = self.request.user.journalist
            form.save()
            # Resto del código de redirección o respuesta
            return redirect('news_service:news_list')
        else:
            return render(request, 'tu_template.html', {'form': form})
