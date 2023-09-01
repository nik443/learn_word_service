from typing import Any, Dict
from ast import literal_eval

from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, FormView
from django.views.decorators.cache import never_cache

from .forms import *
from .utils import *
from .models import *

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


class LearnWords(MixinDataParams, CreateView):
    form_class = CreateWordInMasterDictForm
    template_name = 'learn.html'
    success_url = reverse_lazy('learn_words')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Учить слова')
        return dict(list(context.items()) + list(c_def.items()))
    
    def form_valid(self, form):
        cleaned_word = form.cleaned_data['word']
        cleaned_translation = form.cleaned_data['translation']
        if not MasterDictionaries.objects.filter(word = cleaned_word).exists(): # слова в мастер-словаре должны быть уникальными
            form.save()
        user_dictionary = literal_eval(self.request.user.userdictionaries.dictionary) # получение словаря пользователя
        user_dictionary[cleaned_word] = cleaned_translation
        user_dictionary = dict(sorted(user_dictionary.items())) # сортировка словаря пользователя
        UserDictionaries.objects.filter(user = self.request.user.pk).update(dictionary = user_dictionary) # обновление словаря пользователя
        return redirect('learn_words')

@never_cache
def user_cabinet(request):
    return render(request, 'user_cabinet.html', {'title': 'Личный кабинет', 'menu': MixinDataParams.menu})

class UserDictionary(MixinDataParams, TemplateView):
    template_name = 'user_dictionary.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        dictionary = literal_eval(self.request.user.userdictionaries.dictionary) # получение словаря пользователя
        c_def = self.get_user_context(title='Мой словарь', dictionary = dictionary)
        return dict(list(context.items()) + list(c_def.items()))


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


class Training(MixinDataParams, TemplateView):

    template_name = 'training.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        form_training = TrainingForm(self.request.POST, user=self.request.user)
        c_def = self.get_user_context(title='Training', form=form_training)
        return dict(list(context.items()) + list(c_def.items()))


@never_cache
def result_training(request):

    mistakes = ''
    input_list = list(request.POST.items())[1:] # получили значения и правильный перевод слов
    for i in range(5):
        user_translate = input_list[i][1]
        true_translate = input_list[i][0]
        if user_translate != true_translate: 
            mistakes += f";В {i + 1} поле вы ввели {user_translate}, а правильно {true_translate}"

    if mistakes == '': 
        mistakes = ['Ошибок нет']
    else:
        mistakes = mistakes[1:] # убераем первый ";" из строки, чтобы было проще парсить строку в массив
        mistakes = mistakes.split(';')

    return render(request, 'result_training.html', {
        'title': 'Training results', 
        'menu': MixinDataParams.menu,
        'mistakes': mistakes
        })  











