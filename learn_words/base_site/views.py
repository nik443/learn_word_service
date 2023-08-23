from typing import Any, Dict
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from django.views.decorators.cache import never_cache

from .forms import *
from .utils import *

# Create your views here.

class HomePage(MixinDataParams, TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Домашняя страница')
        return dict(list(context.items()) + list(c_def.items()))


class AboutPage(MixinDataParams, TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='О сайте')
        return dict(list(context.items()) + list(c_def.items()))

@never_cache
def learn_words(request):
    return render(request, 'learn.html', {'title': 'Учить слова', 'menu': MixinDataParams.menu})

@never_cache
def user_cabinet(request):
    return render(request, 'user_cabinet.html', {'title': 'Личный кабинет', 'menu': MixinDataParams.menu})

@never_cache
def user_dictionary(request):
    return render(request, 'user_dictionary.html', {'title': 'Мой словарь', 'menu': MixinDataParams.menu})

class RegisterUser(MixinDataParams, CreateView):    
    form_class = RegisterUserForm 
    template_name = 'register.html' 
    success_url = reverse_lazy('home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(MixinDataParams, LoginView):
    form_class = LoginUserForm 
    template_name = 'login.html' 

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Вход в аккаунт')
        return dict(list(context.items()) + list(c_def.items()))
    
    def get_success_url(self) -> str:
        return reverse_lazy('home')

    
def logout_user(request):
    logout(request) 
    return redirect('login')