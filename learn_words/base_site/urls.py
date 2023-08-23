from django.urls import path, re_path

from .views import *


urlpatterns = [
    path('', home, name='home'),
    path('about/', about, name='about'),
    path('learn/', learn_words, name='learn_words'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('login/', LoginUser.as_view(), name='login'),
]