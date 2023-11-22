from django.utils import timezone
from django.utils.http import urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import EmailMessage


class MixinDataParams:

    menu = [
        {'title': 'На главную', 'url_name': 'base_site:home'},
        {'title': 'Личный кабинет', 'url_name': 'base_site:user_cabinet'}, 
        {'title': 'Учить слова', 'url_name': 'base_site:learn_words'}, 
        {'title': 'О сайте', 'url_name': 'base_site:about'}, 
    ] 

    def get_user_context(self, **kwargs):
        context = kwargs
        if self.request.user.is_authenticated: 
            context['menu'] = self.menu
        else:
            context['menu'] = self.menu[::3] # menu: home, about
        return context
    

def send_email_verify(request, user):
    current_site = get_current_site(request)
    context = {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user)
    }
    message = render_to_string(template_name='base_site/user/registration/verify_email.html', context=context)
    email = EmailMessage(
        'Письмо верификации',
        message,
        to=[user.email]
    )
    email.send()