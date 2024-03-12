from typing import Any
from django import forms
from accounts.forms import MyUserCreateForm
from django.db import transaction
from . import models
from django.contrib.auth import get_user_model
User = get_user_model()


class JournalistSignupForm(MyUserCreateForm):
    # se agregan los campos adicionales para Journalist
    photo = forms.ImageField(required=True)
    description = forms.CharField(widget=forms.Textarea, required=True)

    # la clase Meta hereda del formulario por defecto para User
    class Meta(MyUserCreateForm.Meta):
        model = User

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)

        user.save()
        # creamos una instancia de Journalist y guardamos los datos del formulario
        journalist = models.Journalist.objects.create(
            user=user, photo=self.cleaned_data['photo'], description=self.cleaned_data['description'])

        return user


class NewsCreateForm(forms.ModelForm):
    class Meta:
        model = models.Post
        fields = ['title', 'image', 'content', 'theme']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'other_authors': forms.SelectMultiple(attrs={'class': 'form-control', 'id': 'id_other_authors'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'theme': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False


class AddThemeForm(forms.ModelForm):
    class Meta:
        model = models.Theme
        fields = ['theme']

        widgets = {
            'theme': forms.TextInput(attrs={'class': 'form-control'}),
        }


class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = models.Comment
        fields = ['content']

        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control'})
        }


class ClientSignupForm(MyUserCreateForm):
    bulletin_suscriptor = forms.BooleanField()

    # la clase Meta hereda del formulario por defecto para User
    class Meta(MyUserCreateForm.Meta):
        model = User

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)

        user.save()
        # creamos una instancia de Client y guardamos los datos del formulario
        client = models.Client.objects.create(
            user=user, bulletin_suscriptor=self.cleaned_data['bulletin_suscriptor'])

        return user
