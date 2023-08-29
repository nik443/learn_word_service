from django.urls import path, re_path

from .views import *


urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('about/', AboutPage.as_view(), name='about'),
    path('learn/', LearnWords.as_view(), name='learn_words'),
    path('training/', Training.as_view(), name='training'),
    path('training/result_training/<str:mistakes_list>/', result_training, name='result_training'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('user_cabinet/', user_cabinet, name='user_cabinet'),
    path('user_cabinet/dictionary', UserDictionary.as_view(), name='dictionary'),
]