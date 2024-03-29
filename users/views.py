from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.views.generic import CreateView, TemplateView

from common.views import CommonMixin
from users.forms import UserLoginForm, UserRegisterForm
from users.models import User


class UserLoginView(CommonMixin, SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Авторизация'
    success_message = 'Вы успешно авторизовались!'


class UserRegisterView(CommonMixin, CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    title = 'Регистрация'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('women:index')


class UserProfileView(CommonMixin, LoginRequiredMixin, TemplateView):
    title = 'Профиль'
    template_name = 'users/profile.html'
