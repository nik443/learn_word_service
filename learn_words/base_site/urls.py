from django.urls import path, re_path

from .views import *


app_name = 'base_site' # пространство имен
urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('about/', AboutPage.as_view(), name='about'),
    path('learn/', LearnWords.as_view(), name='learn_words'),
    path('learn/add_word/', addWordInUserDict, name='add_word_in_user_dict'),
    path('training/', Training.as_view(), name='training'),
    path('training/result_training/', result_training, name='result_training'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('user_cabinet/', user_cabinet, name='user_cabinet'),
    path('user_cabinet/dictionary', UserDictionary.as_view(), name='dictionary'),
]