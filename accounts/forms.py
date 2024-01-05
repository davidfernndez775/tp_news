from typing import Any
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django import forms


class UserCreateForm(UserCreationForm):

    class Meta:
        fields = ('username', 'email', 'password1', 'password2')
        model = get_user_model()

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        # crea un label en la pagina HTML
        self.fields['username'].label = 'Display Name'
        self.fields['email'].label = 'Email Address'
