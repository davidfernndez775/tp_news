from typing import Any
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django import forms


class MyUserCreateForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=True, help_text='Required. Enter your first name.')
    last_name = forms.CharField(
        max_length=30, required=True, help_text='Required. Enter your last name.')
    email = forms.EmailField(
        required=True, help_text='Required. Enter your email.')
    # Notese que este group no es groups el campo por defecto de User, el valor lo pasamos en la funcion form_valid() dentro de la clase en el views.py
    group = forms.ModelChoiceField(queryset=Group.objects.all(),
                                   required=True)

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + \
            ('first_name', 'last_name', 'email', 'group')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.group = self.cleaned_data['group']
        if commit:
            user.save()
        return user
