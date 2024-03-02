from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse, reverse_lazy
from django.views import generic
from . import models
from . import forms
from django.contrib.auth import get_user_model
User = get_user_model()  # nopep8
from django.http import request
# from accounts.views import check_user_group


# Create your views here.
# VISTAS RELACIONADAS CON POST

# vista para creacion de temas
class ThemeCreateView(PermissionRequiredMixin, generic.CreateView):
    permission_required = 'news_service.add_theme'
    permission_denied_message = "Sorry, you don't have the permission to access"
    form_class = forms.AddThemeForm
    template_name = 'news_service/add_theme.html'

    def get_success_url(self):
        user = models.Journalist.objects.get(user=self.request.user)
        return reverse_lazy('accounts:board', kwargs={'slug': user.slug})


# vista para ver la lista de news
class NewsListView(generic.ListView):
    model = models.Post
    template_name = 'news_service/news_list.html'

    def get_queryset(self):
        return models.Post.objects.filter(approve=True)


# vista para ver la lista de news pendientes
class UnapproveNewsListView(PermissionRequiredMixin, generic.ListView):
    permission_required = 'news_service.delete_post'
    permission_denied_message = "Sorry, you don't have the permission to access"
    model = models.Post
    template_name = 'news_service/unapprove_news.html'

    def get_queryset(self):
        return models.Post.objects.filter(approve=False)


# vistas de listas filtradas
class PoliticsListView(generic.ListView):
    model = models.Post
    template_name = 'news_service/politics.html'

    def get_queryset(self):
        return models.Post.approve_news.filter(approve=True, theme__theme='politics')


class EconomicsListView(generic.ListView):
    model = models.Post
    template_name = 'news_service/economics.html'

    def get_queryset(self):
        return models.Post.approve_news.filter(theme__theme='economics')


class SportsListViews(generic.ListView):
    model = models.Post
    template_name = 'news_service/sports.html'

    def get_queryset(self):
        return models.Post.approve_news.filter(theme__theme='sports')


# vista detalle
class NewsDetailView(generic.DetailView):
    model = models.Post
    template_name = 'news_service/news_detail.html'

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user_belongs_to_chief = self.request.user.groups.filter(
            name='chief editor').exists()
        context["user_belongs_to_chief"] = user_belongs_to_chief
        context["approve"] = self.object.approve
        return context


# metodos para aprobacion o desaprobacion de noticias
def approve_post(request, pk):
    post = get_object_or_404(models.Post, pk=pk)
    post.approve_post()
    post.publish_post()
    return redirect(reverse('news_service:news_list'))


def hide_post(request, pk):
    post = get_object_or_404(models.Post, pk=pk)
    post.hide_post()
    return redirect(reverse('news_service:unapprove_news'))


# vista para crear noticias
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
