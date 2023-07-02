from women.models import Category

menu = [{'title': "О сайте", 'url_name': 'about'},
        {'title': "Добавить статью", 'url_name': 'add_post'},
        {'title': "Обратная связь", 'url_name': 'feedback'},
        ]


class CommonMixin:
    title = 'Coolsite'

    def get_context_data(self, **kwargs):
        context = super(CommonMixin, self).get_context_data(**kwargs)
        context['title'] = kwargs.get('object') or self.title
        context['categories'] = Category.objects.all()
        context['cat_slug'] = self.kwargs.get('cat_slug')

        user_menu = menu.copy()
        if not self.request.user.is_authenticated:
            user_menu.pop(1)

        context['menu'] = user_menu

        return context
