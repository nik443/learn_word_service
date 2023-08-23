from typing import Any, Dict
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views.decorators.cache import never_cache

from .forms import *
from .utils import *

# Create your views here.

@never_cache
def home(request):
    return render(request, 'index.html', {'title': 'Главная страница', 'menu': MixinDataParams.menu})

@never_cache
def about(request):
    return render(request, 'about.html', {'title': 'О сайте', 'menu': MixinDataParams.menu})

@never_cache
def learn_words(request):
    return render(request, 'learn.html', {'title': 'Учить слова', 'menu': MixinDataParams.menu})


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