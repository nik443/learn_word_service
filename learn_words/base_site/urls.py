from django.urls import path, re_path

from .views import *


app_name = 'base_site' # пространство имен
urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('about/', AboutPage.as_view(), name='about'),
    path('learn/', LearnWords.as_view(), name='learn_words'),
    path('learn/add_word/', add_word_in_user_dict, name='add_word_in_user_dict'),
    path('training/', Training.as_view(), name='training'),
    path('training/result_training/', result_training, name='result_training'),
    path('user_cabinet/', user_cabinet, name='user_cabinet'),
    path('user_cabinet/dictionary', UserDictionary.as_view(), name='dictionary'),
    # login/logout block
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout'),
    # registration block
    path('register/', RegisterUser.as_view(), name='register'),
    path('register/send_message_verify/', SendMessageVerify.as_view(), name='send_message_verify'),
    path('verify_email/<uidb64>/<token>/', VerifyEmail.as_view(), name='verify_email'),
    path('invalid_verify/', InvalidVerify.as_view(), name='invalid_verify'),
    # reset password block
    path("password_reset/", UserPasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/",UserPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", UserPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]