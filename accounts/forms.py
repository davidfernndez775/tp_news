from typing import Any
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class MyUserCreateForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30, required=True, help_text='Required. Enter your first name.')
    last_name = forms.CharField(
        max_length=30, required=True, help_text='Required. Enter your last name.')
    email = forms.EmailField(
        required=True, help_text='Required. Enter your email.')

    class Meta:
        model = User
        fields = UserCreationForm.Meta.fields + \
            ('first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.groups.set(['journalist'])
        if commit:
            user.save()
        return user
