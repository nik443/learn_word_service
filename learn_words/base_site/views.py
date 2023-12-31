from datetime import timedelta

from django.contrib.auth import login, logout
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
    PasswordResetCompleteView,
)
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode
from django.views.generic import CreateView, TemplateView, View
from django.views.decorators.cache import never_cache

from . import models
from . import forms
from . import utils


class HomePage(utils.MixinDataParams, TemplateView):
    template_name = "base_site/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            date_last_added_word_more_1_days = (
                timezone.now()
                - self.request.user.dateslastaddedwordinuserdict.date_last_added_word
            ) > timedelta(days=1)
            if date_last_added_word_more_1_days:
                context["need_learn_words"] = "Пора выучить новые слова!"
            else:
                context[
                    "need_learn_words"
                ] = "Сегодня норма изучения новых слов выполнена"

        c_def = self.get_user_context(title="Домашняя страница")
        return dict(list(context.items()) + list(c_def.items()))


class AboutPage(utils.MixinDataParams, TemplateView):
    template_name = "base_site/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="О сайте")
        return dict(list(context.items()) + list(c_def.items()))


""" ADD WORDS IN USER'S DICTIONARY MECH """


class LearnWords(utils.MixinDataParams, CreateView):
    form_class = forms.CreateWordInMasterDictForm
    template_name = "base_site/user/learnging_and_training/learn.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Учить слова")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        cleaned_word = form.cleaned_data["word"]
        if not models.MasterDictionaries.objects.filter(
            word=cleaned_word
        ).exists():  # слова в мастер-словаре должны быть уникальными
            form.save()
        return redirect("base_site:learn_words")


def add_word_in_user_dict(request):
    user_word = utils.NewUserWord(user=request.user, user_word=request.POST["user_word"])
    result_add_user_word = user_word.try_to_add_user_word_in_his_dict()
    context = {
        "title": "Учить слова",
        "menu": utils.MixinDataParams.menu,
    }

    if result_add_user_word:
        context["user_error"] = result_add_user_word
        return render(
            request, "base_site/user/learnging_and_training/learn.html", context
        )

    return render(
        request, "base_site/user/learnging_and_training/success_add_word.html"
    )


""" ADD WORDS IN USER'S DICTIONARY MECH AND """

""" USER'S CABINET MECH """


@never_cache
def user_cabinet(request):
    return render(
        request,
        "base_site/user/pages/user_cabinet.html",
        {"title": "Личный кабинет", "menu": utils.MixinDataParams.menu},
    )


class UserDictionary(utils.MixinDataParams, TemplateView):
    template_name = "base_site/user/pages//user_dictionary.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        dictionary = {}
        for i in models.UserDictionaries.objects.filter(user=self.request.user):
            dictionary[i.word.word] = i.word.translation

        c_def = self.get_user_context(title="Мой словарь", dictionary=dictionary)
        return dict(list(context.items()) + list(c_def.items()))


""" USER'S CABINET MECH AND"""

""" REGISTRATION/AUTHORIZATION MECH """


class RegisterUser(utils.MixinDataParams, CreateView):
    form_class = forms.RegisterUserForm
    template_name = "base_site/user/registration/register.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Регистрация")
        return dict(list(context.items()) + list(c_def.items()))

    def form_valid(self, form):
        user = form.save()
        utils.send_email_verify(self.request, user)
        models.DatesLastAddedWordInUserDict.objects.create(
            user=user, date_last_added_word=(timezone.now() - timedelta(days=1))
        )
        return redirect("base_site:send_message_verify")


class SendMessageVerify(utils.MixinDataParams, TemplateView):
    template_name = "base_site/user/registration/send_message_verify.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Письмо активации отправлено")
        return dict(list(context.items()) + list(c_def.items()))


class VerifyEmail(View):
    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        if (user is not None) and (default_token_generator.check_token(user, token)):
            user.email_verify = True
            user.save()
            login(request, user)
            return redirect("base_site:home")
        else:
            return redirect("base_site:invalid_verify")

    @staticmethod
    def get_user(uidb64):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = models.MyUser.objects.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            models.MyUser.DoesNotExist,
            forms.ValidationError,
        ):
            user = None
        return user


class InvalidVerify(utils.MixinDataParams, TemplateView):
    template_name = "base_site/user/registration/invalid_verify.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Не удалось активировать аккаунт")
        return dict(list(context.items()) + list(c_def.items()))


class LoginUser(utils.MixinDataParams, LoginView):
    form_class = forms.MyAuthenticationForm
    template_name = "base_site/user/authorization/login.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Вход в аккаунт")
        return dict(list(context.items()) + list(c_def.items()))

    def get_success_url(self) -> str:
        return reverse_lazy("base_site:home")


def logout_user(request):
    logout(request)
    return redirect("base_site:login")


# сброс пароль для входа в аккаунт
class UserPasswordResetView(utils.MixinDataParams, PasswordResetView):
    template_name = "base_site/user/authorization/reset_password.html"
    success_url = reverse_lazy("base_site:password_reset_done")
    email_template_name = "base_site/user/authorization/letter_for_reset_password.html"  # html-письмо с ссылкой на смену пароля
    form_class = forms.UserPasswordResetForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


# успешная отправка письма для восстановления пароля
class UserPasswordResetDoneView(utils.MixinDataParams, PasswordResetDoneView):
    template_name = "base_site/user/authorization/password_reset_done.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


# форма ввода нового пароля
class UserPasswordResetConfirmView(utils.MixinDataParams, PasswordResetConfirmView):
    template_name = "base_site/user/authorization/password_reset_confirm.html"
    success_url = reverse_lazy("base_site:password_reset_complete")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


# подтверждение успешной смены пароля
class UserPasswordResetCompleteView(utils.MixinDataParams, PasswordResetCompleteView):
    template_name = "base_site/user/authorization/password_reset_complete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context()
        return dict(list(context.items()) + list(c_def.items()))


""" REGISTRATION/AUTHORIZATION MECH END """

""" TRAINING USER'S WORD MECH """


class Training(utils.MixinDataParams, TemplateView):
    template_name = "base_site/user/learnging_and_training/training.html"

    def get_context_data(self, **kwargs):
        try:
            user_dict = list(
                models.UserDictionaries.objects.filter(user=self.request.user)[:5]
            )
            form_training = forms.TrainingForm(self.request.POST, words=user_dict)
            c_def = self.get_user_context(title="Training", form=form_training)
        except UnboundLocalError:
            c_def = self.get_user_context(
                title="Training",
                title_error="В вашем словаре слишком мало слов для повторения, минимум 5",
            )
        finally:
            context = super().get_context_data(**kwargs)
            return dict(list(context.items()) + list(c_def.items()))


@never_cache
def result_training(request):
    mistakes = ""
    input_list = list(request.POST.items())[
        1:
    ]  # получили значения и правильный перевод слов
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
            models.MasterDictionaries.objects.get(word=i).userdictionaries_set.filter(
                user=request.user
            ).update(
                last_training_date=timezone.now(), last_training_result=is_true_answer
            )

    if true_answer_list:
        update_user_dict(true_answer_list, True)
    if false_answer_list:
        update_user_dict(false_answer_list, False)

    if mistakes == "":
        mistakes = ["Ошибок нет"]
    else:
        mistakes = mistakes[
            1:
        ]  # убираем первый ";" из строки, чтобы было проще парсить строку в массив
        mistakes = mistakes.split(";")

    return render(
        request,
        "base_site/user/learnging_and_training/result_training.html",
        {
            "title": "Training results",
            "menu": utils.MixinDataParams.menu,
            "mistakes": mistakes,
        },
    )


""" TRAINING USER'S WORD MECH END """
