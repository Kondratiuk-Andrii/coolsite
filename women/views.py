from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import (CreateView, DetailView, FormView, ListView,
                                  TemplateView)

from common.views import CommonMixin
from women.forms import ContactForm, WomenForm
from women.models import Women


class IndexView(CommonMixin, TemplateView):
    template_name = 'index.html'


class WomenView(CommonMixin, ListView):
    model = Women
    template_name = 'women/women.html'

    context_object_name = 'posts'
    allow_empty = False

    paginate_by = 3
    title = 'Women'

    def get_queryset(self):
        queryset = Women.objects.filter(is_published=True).select_related('category')
        queryset = (
            queryset
            if self.kwargs.get('cat_slug') == 'all'
            else queryset.filter(category__slug=self.kwargs['cat_slug'])
        )
        return queryset


class PostDetailView(CommonMixin, DetailView):
    template_name = 'women/post_detail.html'
    model = Women
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'


class AboutView(CommonMixin, TemplateView):
    template_name = 'about.html'
    title = 'О сайте'


class AddPostView(CommonMixin, CreateView):
    form_class = WomenForm
    template_name = 'add_post.html'
    title = 'Добавить статью'
    success_url = reverse_lazy('women:index')


class FeedbackView(CommonMixin, FormView):
    form_class = ContactForm
    template_name = 'feedback.html'
    success_url = reverse_lazy('women:index')
    title = 'Обратная связь'


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')


@login_required()
def add_to_favorite(request, post_slug):
    post = Women.objects.get(slug=post_slug)
    user = request.user
    if post.favorited_by.filter(id=user.id).exists():
        messages.warning(request, 'Пост уже в избранном')
    else:
        post.favorited_by.add(user)
        messages.success(request, 'Пост добавлен в избранное')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required()
def remove_from_favorite(request, post_slug):
    post = Women.objects.get(slug=post_slug)
    user = request.user
    if post.favorited_by.filter(id=user.id).exists():
        user.favorite_posts.remove(post)
        messages.warning(request, 'Пост удален из избранного')
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
