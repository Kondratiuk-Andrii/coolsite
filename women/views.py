from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import *
from .forms import *
from .utils import *

menu = [{'title': "О сайте", 'url_name': 'women:about'},
        {'title': "Добавить статью", 'url_name': 'women:addpage'},
        {'title': "Обратная связь", 'url_name': 'women:contact'},
        {'title': "Войти", 'url_name': 'women:login'}
        ]


class WomenHome(DataMixin, ListView):
    paginate_by = 3
    model = Women  # Передает все записи модели в виде списка
    template_name = 'women/index.html'  # Указываем имя шаблона вместо women/women_list.html
    context_object_name = 'posts'  # Переопределяем название колекции объектов модели

    # extra_context = {}  # Можно передавать ТОЛЬКО статические данные

    def get_context_data(self, *, object_list=None, **kwargs):  # Можно передавать НЕ ТОЛЬКО статические данные
        # context = super().get_context_data(**kwargs)
        # context['title'] = 'Главная страница'
        # context['cat_selected'] = 0
        # return context

        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Главная страница")
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Women.objects.filter(is_published=True)


def about(request):
    return render(request, 'women/about.html', context={'menu': menu})


class AddPage(LoginRequiredMixin, DataMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('women:home')  # Переадресация после успешного создания поста
    login_url = reverse_lazy('women:home')  # Перенаправление for not is_authenticated
    raise_exception = True  # Доступ запрещен for not is_authenticated

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Добавление статьи")
        return dict(list(context.items()) + list(c_def.items()))


def contact(request):
    return render(request, 'women/zaglushka.html', {'title': 'contact', 'menu': menu})


def login(request):
    return render(request, 'women/zaglushka.html', {'title': 'login', 'menu': menu})


class ShowPost(DataMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'  # pk_url_kwarg = 'pk'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return dict(list(context.items()) + list(c_def.items()))


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(
            title='Мировые - ' + str(context['posts'][0].cat),
            cat_selected=context['posts'][0].cat_id,
        )
        return dict(list(context.items()) + list(c_def.items()))

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'], is_published=True)


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
