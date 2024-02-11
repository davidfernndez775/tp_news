from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect
from news_service.forms import JournalistSignupForm
from django.contrib.auth.models import User, Group
from news_service.models import Journalist
from accounts.forms import MyUserCreateForm
from django.contrib.auth.models import User
# Create your views here.


class SignUp(PermissionRequiredMixin, CreateView):
    # se definen los permisos requeridos para acceder
    permission_required = "accounts.add_user"
    permission_denied_message = "Sorry, you don't have the permission to access"
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

# # esta variante borra al usuario de la base de datos, no recomendado
# class JournalistDeleteView(PermissionRequiredMixin, DeleteView):
#     permission_required = "accounts.delete_user"
#     template_name = 'accounts/delete_journalist.html'
#     model = User
#     success_url = reverse_lazy("news_service:journalists_list")

# con esta forma en lugar de borrar al usuario de la base de datos se establece el parametro is_active en False, con lo cual ya no se puede loguear en el sitio, recomendado


class UserConfirmDelete(PermissionRequiredMixin, DetailView):
    permission_required = "accounts.delete_user"
    model = User
    template_name = 'accounts/delete_journalist.html'
    permission_denied_message = "Sorry, you don't have the permission to access"

    # funcion para poner is_active en False
    def delete_user(self, pk):
        user = User.objects.get(pk=pk)
        user.is_active = False
        user.save()
        return redirect('news_service:journalists_list')

    # como la confirmacion y la eliminacion se hacen en la misma pagina, es necesario usar dispath de tal manera que cuando se reciba un GET muestre la pagina, y cuando reciba un POST (o sea se ejecuta el formulario de eliminacion) devuelva la ejecucion de la funcion delete_user que esta dentro de la misma clase UserConfirmDelete
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            return self.delete_user(pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)


class UserUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = "accounts.change_user"
    permission_denied_message = "Sorry, you don't have the permission to access"
    login_url = '/login/'
    template_name = 'accounts/signup'
    # redirect_field_name = 'news_service/board.html'
    model = User
    form_class = JournalistSignupForm
    success_url = '/news_service/board.html'
