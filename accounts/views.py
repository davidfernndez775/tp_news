from django.shortcuts import render
from django.views.generic import CreateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from news_service.forms import JournalistSignupForm
from django.contrib.auth.models import User, Group
from news_service.models import Journalist
from accounts.forms import MyUserCreateForm
# Create your views here.


class SignUp(PermissionRequiredMixin, CreateView):
    # se definen los permisos requeridos para acceder
    permission_required = "accounts.add_user"
    form_class = JournalistSignupForm
    # se usa reverse_lazy para garantizar que se guarde el signup antes de ir al login
    success_url = reverse_lazy('news_service:journalists_list')
    template_name = 'accounts/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)

        # Crear o recuperar el objeto Journalist asociado al usuario, para que exista cuando le asignemos los grupos a los que pertenece
        journalist, created = Journalist.objects.get_or_create(
            user=self.object)

        # asignamos el grupo guardado en el campo group del formulario al atributo groups de la clase User, esto es asi porque si no tenemos problemas con la relacion Many to Many
        self.object.groups.add(self.object.group)

        return response


class JournalistDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "accounts.delete_user"
    template_name = 'accounts/delete_journalist.html'
    model = User
    success_url = reverse_lazy("news_service:journalists_list")
# TODO falta la logica para una vez que se borra un usuario dejar su informacion en los post relacionados
