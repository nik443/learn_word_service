class MixinDataParams:

    menu = [
        {'title': 'На главную', 'url_name': 'home'},
        {'title': 'Личный кабинет', 'url_name': 'user_cabinet'}, 
        {'title': 'Учить слова', 'url_name': 'learn_words'}, 
        {'title': 'О сайте', 'url_name': 'about'}, 
    ] 

    def get_user_context(self, **kwargs):
        context = kwargs
        if self.request.user.is_authenticated: 
            context['menu'] = self.menu
        else:
            context['menu'] = self.menu[::3] # menu: home, about
        return context