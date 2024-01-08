from ast import literal_eval
import random

from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from django.forms.utils import ErrorList

from .models import *
from .utils import send_email_verify


# Create your models here.
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Ник', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = models.MyUser
        fields = ('username', 'email', 'password1', 'password2')


class MyAuthenticationForm(AuthenticationForm):

    def clean(self):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]

        self.user_cache = authenticate(
            self.request, username=username, password=password
        )
        if self.user_cache is not None:
            if self.user_cache.email_verify:
                return self.cleaned_data
            else:
                send_email_verify(self.request, self.user_cache)
                raise ValidationError(
                    'Неподтвержденный email, на вашу почту отправленно дополнительное письмо подтверждения!',
                    code="inactive",
                )
        else:
            raise ValidationError('Неправильно введен пароль или логин')


class CreateWordInMasterDictForm(forms.ModelForm):
    class Meta:
        model = models.MasterDictionaries
        fields = ['word']


class TrainingForm(forms.Form):

    def __init__(self, *args, **kwargs):
        self.words = kwargs.pop('words', None)

        # label - перевод
        word0 = forms.CharField(label=self.words[0].word.translation,
                                widget=forms.TextInput(attrs={'class': 'form-input'}))
        word1 = forms.CharField(label=self.words[1].word.translation,
                                widget=forms.TextInput(attrs={'class': 'form-input'}))
        word2 = forms.CharField(label=self.words[2].word.translation,
                                widget=forms.TextInput(attrs={'class': 'form-input'}))
        word3 = forms.CharField(label=self.words[3].word.translation,
                                widget=forms.TextInput(attrs={'class': 'form-input'}))
        word4 = forms.CharField(label=self.words[4].word.translation,
                                widget=forms.TextInput(attrs={'class': 'form-input'}))

        # name - правильное значение
        super(TrainingForm, self).__init__(*args, **kwargs)
        self.fields[self.words[0].word.word] = word0
        self.fields[self.words[1].word.word] = word1
        self.fields[self.words[2].word.word] = word2
        self.fields[self.words[3].word.word] = word3
        self.fields[self.words[4].word.word] = word4


class UserPasswordResetForm(PasswordResetForm):

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            return email
        raise ValidationError('Пользователя с таким email не существует на сервисе')
