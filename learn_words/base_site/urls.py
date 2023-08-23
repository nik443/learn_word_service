from django.urls import path, re_path

from .views import *


urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('about/', AboutPage.as_view(), name='about'),
    path('learn/', learn_words, name='learn_words'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    path('user_cabinet/', user_cabinet, name='user_cabinet'),
    path('user_cabinet/dictionary', user_dictionary, name='dictionary'),
]