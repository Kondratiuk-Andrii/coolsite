from django.urls import path

from women.views import IndexView, PostDetailView, WomenView

app_name = "women"

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("category/<slug:cat_slug>", WomenView.as_view(), name="category"),
    path("post/<slug:post_slug>", PostDetailView.as_view(), name="post_detail"),
]
