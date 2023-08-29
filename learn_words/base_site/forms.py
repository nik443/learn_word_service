from ast import literal_eval

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

    word0 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input', 
        'data-word-translate': ''}))
    word1 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input', 
        'data-word-translate': ''}))
    word2 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input',
        'data-word-translate': ''}))
    word3 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input',
        'data-word-translate': ''}))
    word4 = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-input',
        'data-word-translate': ''}))

    """ def clean_word0(self):
        word = self.cleaned_data['word0']
        print(dir(forms.CharField))
        if word != '':
            raise ValidationError('Верное написание: dadfadfadf')
        return word """