class MixinDataParams:

    menu = [{'title': 'На главную', 'url_name': 'home'},
        {'title': 'О сайте', 'url_name': 'about'}, 
        {'title': 'Учить слова', 'url_name': 'learn_words'}, 
    ] 

    def get_user_context(self, **kwargs):
        context = kwargs
        context['menu'] = self.menu
        return context
    