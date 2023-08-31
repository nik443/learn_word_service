from ast import literal_eval
from random import sample

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

    user_dict = UserDictionaries.objects.get(user_id=1).dictionary
    user_dict = literal_eval(user_dict)
    user_dict = list(user_dict.items())
    user_dict = sample(user_dict, 5)

    word0 = forms.CharField(label=user_dict[0][1], widget=forms.TextInput(attrs={
        'class': 'form-input', 
        'data-word-translate': user_dict[0][0]}))
    word1 = forms.CharField(label=user_dict[1][1], widget=forms.TextInput(attrs={
        'class': 'form-input', 
        'data-word-translate': user_dict[1][0]}))
    word2 = forms.CharField(label=user_dict[2][1], widget=forms.TextInput(attrs={
        'class': 'form-input',
        'data-word-translate': user_dict[2][0]}))
    word3 = forms.CharField(label=user_dict[3][1], widget=forms.TextInput(attrs={
        'class': 'form-input',
        'data-word-translate': user_dict[3][0]}))
    word4 = forms.CharField(label=user_dict[4][1], widget=forms.TextInput(attrs={
        'class': 'form-input',
        'data-word-translate': user_dict[4][0]}))
