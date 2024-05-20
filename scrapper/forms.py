from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .validators import validate_email_username


class SignUpForm(UserCreationForm):

    username = forms.EmailField(help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ("username", "password1", "password2")


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(widget=forms.EmailField())
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
