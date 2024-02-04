from django.shortcuts import render
from django.views.generic import CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from news_service.forms import JournalistSignupForm
# Create your views here.


class SignUp(PermissionRequiredMixin, CreateView):
    permission_required = "accounts.user.can_add_user"
    form_class = JournalistSignupForm
    # se usa reverse_lazy para garantizar que se guarde el signup antes de ir al login
    success_url = reverse_lazy('news_service:journalists_list')
    template_name = 'accounts/signup.html'
