import requests
from bs4 import BeautifulSoup

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from . import models


class MixinDataParams:
    menu = [
        {"title": "На главную", "url_name": "base_site:home"},
        {"title": "Личный кабинет", "url_name": "base_site:user_cabinet"},
        {"title": "Учить слова", "url_name": "base_site:learn_words"},
        {"title": "О сайте", "url_name": "base_site:about"},
    ]

    def get_user_context(self, **kwargs):
        context = kwargs
        if self.request.user.is_authenticated:
            context["menu"] = self.menu
        else:
            context["menu"] = self.menu[::3]  # menu: home, about
        return context


def send_email_verify(request, user):
    current_site = get_current_site(request)
    context = {
        "user": user,
        "domain": current_site.domain,
        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
        "token": default_token_generator.make_token(user),
    }
    message = render_to_string(
        template_name="base_site/user/registration/verify_email.html", context=context
    )
    email = EmailMessage("Письмо верификации", message, to=[user.email])
    email.send()


class NewUserWord:
    def __init__(self, user, user_word):
        self.user = user
        self.user_word = user_word

    def try_to_add_user_word_in_his_dict(self) -> str:
        try:
            word = get_object_or_404(models.MasterDictionaries, word=self.user_word)
            if word.userdictionaries_set.filter(user=self.user).exists():
                return "Введенное слово уже есть в вашем словаре"

            NewUserWord.add_new_word_in_master_and_user_dict(self.user, self.user_word)

        except Http404:
            translate_from_web = NewUserWord.check_user_word_in_web(self.user_word)
            if not translate_from_web:
                return "Введенного слова не существует, может это сленг..."

            new_word = models.MasterDictionaries(
                word=self.user_word, translation=translate_from_web
            )
            new_word.save()
            NewUserWord.add_new_word_in_master_and_user_dict(self.user, new_word)

    @staticmethod
    def add_new_word_in_master_and_user_dict(user: models.MyUser, word: str) -> None:
        models.UserDictionaries(user=user, word=word).save()
        models.DatesLastAddedWordInUserDict.objects.filter(user=user).update(
            date_last_added_word=timezone.now()
        )

    @staticmethod
    def check_user_word_in_web(user_word: str) -> str | None:
        url = "https://wooordhunt.ru/word/" + user_word
        response = requests.get(url, verify=False)
        soup = BeautifulSoup(response.text, "lxml")
        try:
            translate = soup.find("div", class_="t_inline_en").text
            return translate[: translate.find(",")]
        except AttributeError:
            return
