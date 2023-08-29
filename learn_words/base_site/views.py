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


class Training(MixinDataParams, FormView):

    template_name = 'training.html'
    success_url = reverse_lazy('learn_words')
    form_class = TrainingForm

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        dictionary = literal_eval(self.request.user.userdictionaries.dictionary)
        training_keys = list(dictionary.keys())
        training_words = list(dictionary.values())
        for i in range(5):
            input = self.form_class.declared_fields['word' + str(i)]
            input.label = training_words[i]
            input.widget.attrs['data-word-translate'] = training_keys[i]
            
        c_def = self.get_user_context(title='Тренировка слов')
        return dict(list(context.items()) + list(c_def.items()))
    
    def form_valid(self, form) -> HttpResponse:
        mistakes = ''
        for i in range(5):
            user_translate_word = self.request.POST['word' + str(i)]
            true_translate_word = form.declared_fields['word' + str(i)].widget.attrs['data-word-translate']
            if user_translate_word != true_translate_word:
                mistakes += f";В {i} поле вы ввели {user_translate_word}, а правильно {true_translate_word}"

        if mistakes == '': 
            mistakes = 'Ошибок нет'
        else:
            mistakes = mistakes[1:] # убераем первый ";" из строки, чтобы было проще парсить строку в массив
        return redirect('result_training', mistakes_list = mistakes)


@never_cache
def result_training(request, mistakes_list):
    return render(request, 'result_training.html', {
        'title': 'Результаты тренировки', 
        'menu': MixinDataParams.menu,
        'mistakes_list': mistakes_list 
        })  

""" class ResultTraining(MixinDataParams, TemplateView):
    template_name = 'result_training.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Мой словарь', )
        return dict(list(context.items()) + list(c_def.items())) """
