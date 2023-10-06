from django.utils import timezone

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
    

    