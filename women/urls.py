from django.urls import path

from women.views import IndexView, PostDetailView, WomenView, add_to_favorite, remove_from_favorite

app_name = "women"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("category/<slug:cat_slug>", WomenView.as_view(), name="category"),
    path("post/<slug:post_slug>", PostDetailView.as_view(), name="post_detail"),

    path('post/<slug:post_slug>/favorite_add', add_to_favorite, name='add_to_favorite'),
    path('post/<slug:post_slug>/favorite_remove', remove_from_favorite, name='remove_from_favorite'),
]
