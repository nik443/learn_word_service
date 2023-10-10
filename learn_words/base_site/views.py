from datetime import timedelta
from typing import Any, Dict

from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.core.exceptions import ValidationError
from django.forms.models import BaseModelForm
from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, TemplateView, FormView
from django.views.decorators.cache import never_cache

from .forms import *
from .utils import *
from .models import *

# Create your views here.

class HomePage(MixinDataParams, TemplateView):
    template_name = 'base_site/index.html'
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            date_last_added_word_more_1_days = (timezone.now() - self.request.user.dateslastaddedwordinuserdict.date_last_added_word) > timedelta(days=1)
            if date_last_added_word_more_1_days:
                context['need_learn_words'] = 'Пора выучить новые слова!'
            else: 
                context['need_learn_words'] = 'Сегодня норма изучения новых слов выполнена'

        c_def = self.get_user_context(title='Домашняя страница')
        return dict(list(context.items()) + list(c_def.items()))


class AboutPage(MixinDataParams, TemplateView):
    template_name = 'base_site/about.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='О сайте')
        return dict(list(context.items()) + list(c_def.items()))


""" ADD WORDS IN USER'S DICTIONARY MECH """

class LearnWords(MixinDataParams, CreateView):
    form_class = CreateWordInMasterDictForm
    template_name = 'base_site/learn.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Учить слова')
        return dict(list(context.items()) + list(c_def.items()))
    
    def form_valid(self, form):
        cleaned_word = form.cleaned_data['word']
        if not MasterDictionaries.objects.filter(word = cleaned_word).exists(): # слова в мастер-словаре должны быть уникальными
            form.save()
        return redirect('base_site:learn_words')
    

def addWordInUserDict(request):
    user_word = request.POST['user_word']
    user_error = ''

    try:
        word = get_object_or_404(MasterDictionaries, word=user_word)
        if word.userdictionaries_set.filter(user=request.user).exists(): # проверка наличия введенного слова в словаре пользователя 
            user_error = 'Введенное слово уже есть в вашем словаре'
        else:
            UserDictionaries(user=request.user, word=word).save() # сохранение слова
            DatesLastAddedWordInUserDict.objects.filter(user=request.user).update(date_last_added_word=timezone.now()) # обновление даты последнего добавления слова
    except Http404:
        user_error = 'Введенного слова не существует, может это сленг...'

    context = {
            'title': 'Учить слова', 
            'menu': MixinDataParams.menu,
        }
    if user_error:
        context['user_error'] = user_error
        return render(request, 'base_site/learn.html', context)
    else:
        return render(request, 'base_site/success_add_word.html')

""" ADD WORDS IN USER'S DICTIONARY MECH AND """

""" USER'S CABINET MECH """

@never_cache
def user_cabinet(request):
    return render(request, 'base_site/user_cabinet.html', {'title': 'Личный кабинет', 'menu': MixinDataParams.menu})

class UserDictionary(MixinDataParams, TemplateView):
    template_name = 'base_site/user_dictionary.html'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        dictionary = {}
        for i in UserDictionaries.objects.filter(user=self.request.user):
            dictionary[i.word.word] = i.word.translation

        c_def = self.get_user_context(title='Мой словарь', dictionary=dictionary)
        return dict(list(context.items()) + list(c_def.items()))

""" USER'S CABINET MECH AND"""

class RegisterUser(MixinDataParams, CreateView):    
    form_class = RegisterUserForm 
    template_name = 'base_site/register.html' 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Регистрация')
        return dict(list(context.items()) + list(c_def.items()))
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        DatesLastAddedWordInUserDict.objects.create(user=self.request.user, date_last_added_word=(timezone.now() - timedelta(days=1)))
        return redirect('base_site:home')


class LoginUser(MixinDataParams, LoginView):
    form_class = LoginUserForm 
    template_name = 'base_site/login.html' 

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title='Вход в аккаунт')
        return dict(list(context.items()) + list(c_def.items()))
    
    def get_success_url(self) -> str:
        return reverse_lazy('base_site:home')

    
def logout_user(request):
    logout(request) 
    return redirect('base_site:login')

""" TRAINING USER'S WORD MECH """
class Training(MixinDataParams, TemplateView):

    template_name = 'base_site/training.html'

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user_dict = list(get_list_or_404(UserDictionaries, user=self.request.user)[:5])
        form_training = TrainingForm(self.request.POST, words=user_dict)
        c_def = self.get_user_context(title='Training', form=form_training)
        return dict(list(context.items()) + list(c_def.items()))
        """ try:
            user_dict = list(get_list_or_404(UserDictionaries, user=self.request.user)[:5]) # получить слова для тренировки
            form_training = TrainingForm(self.request.POST, words=user_dict)
            c_def = self.get_user_context(title='Training', form=form_training)
        except UnboundLocalError:
            c_def = self.get_user_context(title='Training', title_error='В вашем словаре слишком мало слов для повторения, минимум 5')
        finally:
            return dict(list(context.items()) + list(c_def.items())) """

@never_cache
def result_training(request):

    mistakes = ''
    input_list = list(request.POST.items())[1:] # получили значения и правильный перевод слов
    true_answer_list = []
    false_answer_list = []
    for i in range(5):
        user_translate = input_list[i][1]
        true_translate = input_list[i][0]
        if user_translate != true_translate: 
            mistakes += f";В {i + 1} поле вы ввели {user_translate}, а правильно {true_translate}"
            false_answer_list.append(true_translate)
        else:
            true_answer_list.append(true_translate)

    def update_user_dict(answer_list, is_true_answer):
        for i in answer_list: 
            MasterDictionaries.objects.get(word=i).userdictionaries_set.filter(user=request.user).update(last_training_date=timezone.now(), last_training_result=is_true_answer)
    
    if true_answer_list: update_user_dict(true_answer_list, True)
    if false_answer_list: update_user_dict(false_answer_list, False)

    if mistakes == '': 
        mistakes = ['Ошибок нет']
    else:
        mistakes = mistakes[1:] # убираем первый ";" из строки, чтобы было проще парсить строку в массив
        mistakes = mistakes.split(';')

    return render(request, 'base_site/result_training.html', {
        'title': 'Training results', 
        'menu': MixinDataParams.menu,
        'mistakes': mistakes
        })  

""" TRAINING USER'S WORD MECH END """









