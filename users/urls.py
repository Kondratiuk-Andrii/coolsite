from django.contrib.auth.decorators import login_required
from django.urls import path

from users.views import login
from django.contrib.auth.views import LogoutView

app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('logout/', login_required(LogoutView.as_view()), name='logout'),
]
