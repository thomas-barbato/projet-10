from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django import forms
from .models import Users
import re

from .validators.check_data import CheckPasswordPolicy


class UserCreationForm(forms.ModelForm):
    password = forms.CharField(
        style={"input_type": "password"},
        label="Mot de passe",
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        style={"input_type": "password"},
        label="Confirmation du mot de passe",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = Users
        fields = ("email", "password", "password2", "first_name", "last_name")

    def clean_password2(self):
        # Check that the two password entries match
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        CheckPasswordPolicy().validate(password=password, password2=password2)
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
