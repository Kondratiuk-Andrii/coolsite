from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import *
from captcha.fields import CaptchaField


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = 'Категория не выбрана'
        # self.fields['slug'].disabled = True

    class Meta:
        model = Women
        fields = ('title', 'content', 'photo', 'is_published', 'cat')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')
        return title

    # title = forms.CharField(max_length=255, label='Заголовок', widget=forms.TextInput(attrs={'class': 'form-input'}))
    # slug = forms.SlugField(max_length=255, label='url')  # disabled=True
    # content = forms.CharField(widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}), label='Содержимое')
    # is_published = forms.BooleanField(label='Публикация', required=False, initial=True)
    # cat = forms.ModelChoiceField(queryset=Category.objects.all(), label='Категория', empty_label='Категория не выбрана')


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(label="Имя", widget=forms.TextInput(attrs={"class": "form-input"}))
    last_name = forms.CharField(label="Фамилия", widget=forms.TextInput(attrs={"class": "form-input"}))
    username = forms.CharField(label="Логин", widget=forms.TextInput(attrs={"class": "form-input"}))
    email = forms.EmailField(label="Email", widget=forms.TextInput(attrs={"class": "form-input"}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(attrs={"class": "form-input"}))
    password2 = forms.CharField(label="Повтор пароля", widget=forms.PasswordInput(attrs={"class": "form-input"}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин",
                               widget=forms.TextInput(attrs={"class": "form-input", "placeholder": "Логин"}))
    password = forms.CharField(label="Пароль",
                               widget=forms.PasswordInput(attrs={"class": "form-input", "placeholder": "Пароль"}))


class ContactForm(forms.Form):
    name = forms.CharField(label="Имя", max_length=255)
    email = forms.EmailField(label="Email")
    content = forms.CharField(label="Content", widget=forms.Textarea(attrs={"cols": 60, "rows": 10}))
    captcha = CaptchaField(label="Captcha")
