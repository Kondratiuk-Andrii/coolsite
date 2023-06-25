from django.urls import path

from women.views import post_detail, index, women

app_name = 'women'

urlpatterns = [
    path('', women, name='index'),
    # path('', WomenView.as_view(), name='index'),
    path('category/<slug:cat_slug>', women, name='category'),
    path('post/<slug:post_slug>', post_detail, name='post_detail'),

]
