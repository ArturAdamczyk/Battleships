from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class NewGameForm(forms.Form):
    name = forms.CharField(label='Name', max_length=200)


class MessageForm(forms.Form):
    message = forms.CharField(label='Message', max_length=200)


class SignUpForm(UserCreationForm):
    nickname = forms.CharField(max_length=120, required=True)
    email = forms.EmailField(max_length=120, required=False)

    class Meta:
        model = User
        fields = ('username', 'nickname', 'email', 'password1', 'password2', )