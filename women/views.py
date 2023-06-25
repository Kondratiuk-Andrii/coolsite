from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404, redirect

from women.forms import WomenForm
from women.models import Women, Category


def index(request, cat_slug=None):
    context = {
        'title': 'Coolsite',
        'cat_slug': cat_slug,
    }
    return render(request, 'women/index.html', context)


def women(request, cat_slug=None):
    context = {
        'title': 'Coolsite',
        'cat_slug': cat_slug,
    }
    return render(request, 'women/women.html', context)


def post_detail(request, post_slug):
    post = get_object_or_404(Women, slug=post_slug)
    context = {
        'title': post.title,
        'post': post,
    }
    return render(request, 'women/post_detail.html', context)


def about(request):
    context = {
        'title': 'О сайте',
    }
    return render(request, 'women/about.html', context)


def feedback(request):
    context = {
        'title': 'Обратная связь',
    }
    return render(request, 'women/feedback.html', context)


def add_post(request):
    if request.method == 'POST':
        form = WomenForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('women:index')
    else:
        form = WomenForm()
    context = {
        'form': form,
        'title': 'Добавить пост',
    }
    return render(request, 'women/add_post.html', context)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
