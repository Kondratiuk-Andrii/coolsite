from django import template
from django.db.models import Count
from django.http import Http404

from women.models import Women, Category

register = template.Library()


#
# @register.simple_tag(name='get_categories')
# def get_categories(pk=None):
#     if not pk:
#         return Category.objects.all()
#     else:
#         return Category.objects.filter(pk=pk)


@register.inclusion_tag('women/list_categories.html')
def show_categories(sort=None, cat_slug=None):
    if not sort:
        categories = Category.objects.all()
    else:
        if 'count' in sort:
            categories = Category.objects.annotate(count=Count('women')).order_by(f'{sort}')
        else:
            categories = Category.objects.order_by(sort)
    return {'categories': categories, 'cat_slug': cat_slug}


@register.inclusion_tag('women/list_posts.html')
def show_posts(sort=None, cat_slug=None):
    if cat_slug:
        posts = Women.objects.filter(category__slug=cat_slug)
    else:
        posts = Women.objects.all()

    if sort:
        posts = posts.order_by(sort)

    if not posts.exists():
        raise Http404()

    return {
        'posts': posts
        .select_related('category')
        .only('title', 'content', 'photo', 'time_update', 'category__name', )
    }
