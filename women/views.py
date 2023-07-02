from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, TemplateView

from common.views import CommonMixin
from women.forms import WomenForm
from women.models import Women


class IndexView(CommonMixin, TemplateView):
    template_name = 'women/index.html'


class WomenView(CommonMixin, ListView):
    model = Women
    template_name = 'women/women.html'
    context_object_name = 'posts'
    title = 'Women'
    allow_empty = True
    paginate_by = 3

    def get_queryset(self):
        queryset = (
            Women.objects
            .filter(is_published=True)
            .order_by('-time_create')
            .select_related('category')
        )
        queryset = (queryset if self.kwargs.get('cat_slug') == 'all'
                    else queryset.filter(category__slug=self.kwargs['cat_slug']))
        return queryset


class PostDetailView(CommonMixin, DetailView):
    template_name = 'women/post_detail.html'
    model = Women
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'


class AboutView(CommonMixin, TemplateView):
    template_name = 'women/about.html'
    title = 'О сайте'


class AddPostView(CommonMixin, CreateView):
    form_class = WomenForm
    template_name = 'women/add_post.html'
    title = 'Добавить статью'
    success_url = reverse_lazy('index')


class FeedbackView(CommonMixin, TemplateView):
    template_name = 'women/feedback.html'
    title = 'Обратная связь'


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Страница не найдена</h1>')
