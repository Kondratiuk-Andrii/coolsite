from django.urls import path
from .views import *

app_name = 'women'

urlpatterns = [
    path('', WomenHome.as_view(), name='home'),

    path('about/', about, name='about'),
    path('addpage/', AddPage.as_view(), name='addpage'),
    path('contact/', contact, name='contact'),
    path('login/', login, name='login'),
    path('register/', RegisterUser.as_view(), name='register'),

    path('category/<slug:cat_slug>/', WomenCategory.as_view(), name='category'),
    path('post/<slug:post_slug>/', ShowPost.as_view(), name='post'),
]
