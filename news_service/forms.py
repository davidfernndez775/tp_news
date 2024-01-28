from typing import Any
# from accounts.forms import UserCreateForm
from django import forms
from . import models


class JournalistCreateForm(forms.ModelForm):
    class Meta:
        fields = ('photo', 'description')
        model = models.Journalist
