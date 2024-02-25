from typing import Any
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django import forms
from news_service.models import Journalist


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


class MyUserUpdateForm(forms.ModelForm):
    # Agregar los campos adicionales que desees del modelo User
    username = forms.CharField(
        required=True, help_text='Required. Enter your new username.')
    email = forms.EmailField(
        required=True, help_text='Required. Enter your new email.')

    class Meta:
        model = Journalist
        # Campos del modelo Profile que deseas incluir en el formulario
        fields = ['description', 'photo']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Agregar campos del modelo User al formulario
        self.fields['username'].initial = self.instance.user.username
        self.fields['email'].initial = self.instance.user.email

    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get('username')
        email = cleaned_data.get('email')

        # Validar campos del modelo User si es necesario
        # Por ejemplo, puedes agregar validaciones de longitud, unicidad, etc.

        return cleaned_data

    def save(self, commit=True):
        # Guardar datos del modelo User y del modelo Journalist
        user = self.instance.user
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            self.instance.save()
        return self.instance
