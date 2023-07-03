from captcha.fields import CaptchaField
from django import forms
from django.core.exceptions import ValidationError

from women.models import Women


class WomenForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].max_length = 255
        self.fields['title'].label = 'Заголовок'
        self.fields['content'].label = 'Текст статьи'
        self.fields['photo'].label = 'Фото'
        self.fields['photo'].required = False
        self.fields['category'].label = 'Категория'
        self.fields['category'].empty_label = 'Категория не выбрана'

    class Meta:
        model = Women
        fields = ('title', 'content', 'photo', 'category')
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'content': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 200:
            raise ValidationError('Длина превышает 200 символов')
        return title


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(
        label='Содержимое', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10})
    )
    captcha = CaptchaField()
