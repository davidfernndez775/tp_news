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
# VISTAS RELACIONADAS CON NEWS

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
    success_url = "//"


# VISTAS RELACIONADAS CON JOURNALISTS

class BoardView(LoginRequiredMixin, generic.DetailView):
    model = models.Journalist
    template_name = 'news_service/board.html'

    # funcion para agregar datos a la vista
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # comprobamos si el usuario pertenece al grupo chief editor
        user_belongs_to_chief = self.request.user.groups.filter(
            name='chief editor').exists()
        # devolvemos el resultado de la comprobacion a la template tag que se va a usar en el template
        context['user_belongs_to_chief'] = user_belongs_to_chief
        return context


class JournalistsListView(generic.ListView):
    model = models.Journalist
    template_name = 'news_service/journalists.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user_belongs_to_chief = self.request.user.groups.filter(
            name='chief editor').exists()
        context["user_belongs_to_chief"] = user_belongs_to_chief
        return context


def check_user_group(request):
    user_belongs_to_chief = request.user.groups.filter(
        name='chief editor').exists()
    return render(request, {'user_belongs_to_group': user_belongs_to_chief})


class UnactiveJournalistsListView(PermissionRequiredMixin, generic.ListView):
    permission_required = "accounts.add_user"
    permission_denied_message = "Sorry, you don't have the permission to access"
    model = models.Journalist
    template_name = 'news_service/journalists.html'
