from django.urls import path, re_path

from . import views

app_name = 'base_site'  # пространство имен
urlpatterns = [
    path('', views.HomePage.as_view(), name='home'),
    path('about/', views.AboutPage.as_view(), name='about'),
    path('learn/', views.LearnWords.as_view(), name='learn_words'),
    path('learn/add_word/', views.add_word_in_user_dict, name='add_word_in_user_dict'),
    path('training/', views.Training.as_view(), name='training'),
    path('training/result_training/', views.result_training, name='result_training'),
    path('user_cabinet/', views.user_cabinet, name='user_cabinet'),
    path('user_cabinet/dictionary', views.UserDictionary.as_view(), name='dictionary'),
    # login/logout block
    path('login/', views.LoginUser.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    # registration block
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('register/send_message_verify/', views.SendMessageVerify.as_view(), name='send_message_verify'),
    path('verify_email/<uidb64>/<token>/', views.VerifyEmail.as_view(), name='verify_email'),
    path('invalid_verify/', views.InvalidVerify.as_view(), name='invalid_verify'),
    # reset password block
    path("password_reset/", views.UserPasswordResetView.as_view(), name="password_reset"),
    path("password_reset/done/", views.UserPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views.UserPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("reset/done/", views.UserPasswordResetCompleteView.as_view(), name="password_reset_complete"),
]