from ast import literal_eval
import random

from typing import Any, Dict, Mapping, Optional, Type, Union
from django import forms
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms.utils import ErrorList

from .models import *


# Create your models here.
class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Ник', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Ник', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class CreateWordInMasterDictForm(forms.ModelForm):
    class Meta:
        model = MasterDictionaries
        fields = ['word', 'translation']

      
class TrainingForm(forms.Form):

    def __init__(self, *args, **kwargs):

        self.user = kwargs.pop('user', None)
        self.dictionary = literal_eval(self.user.userdictionaries.dictionary)
        self.dictionary = list(self.dictionary.items())
        self.words = random.sample(self.dictionary, 5)

        word0 = forms.CharField(label=self.words[0][1], widget=forms.TextInput(attrs={'class': 'form-input'}))
        word1 = forms.CharField(label=self.words[1][1], widget=forms.TextInput(attrs={'class': 'form-input'}))
        word2 = forms.CharField(label=self.words[2][1], widget=forms.TextInput(attrs={'class': 'form-input'}))
        word3 = forms.CharField(label=self.words[3][1], widget=forms.TextInput(attrs={'class': 'form-input'}))
        word4 = forms.CharField(label=self.words[4][1], widget=forms.TextInput(attrs={'class': 'form-input'}))

        super(TrainingForm, self).__init__(*args, **kwargs)
        self.fields[self.words[0][0]] = word0
        self.fields[self.words[1][0]] = word1
        self.fields[self.words[2][0]] = word2
        self.fields[self.words[3][0]] = word3
        self.fields[self.words[4][0]] = word4