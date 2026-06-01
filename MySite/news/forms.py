from django import forms
from .models import News, Category, Comment
import re
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField


class ContactForm(forms.Form):
    subject = forms.CharField(
        label='Тема',
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Тема сообщения"})
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "your@email.com"})
    )
    content = forms.CharField(
        label='Сообщение',
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 5, "placeholder": "Ваше сообщение..."})
    )
    captcha = CaptchaField(label='Капча')


class NewsForm(forms.ModelForm):
    photo = forms.ImageField(label='Фото', required=False, widget=forms.FileInput(attrs={"class": "form-control"}))

    class Meta:
        model = News
        fields = ['title', 'content', 'is_published', 'category', 'photo']
        widgets = {
            'title': forms.TextInput(attrs={"class": "form-control"}),
            'content': forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5
            }),
            'category': forms.Select(attrs={"class": "form-control"}),
            'is_published': forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
        labels = {
            'title': 'Наименование:',
            'content': 'Контент:',
            'is_published': 'Опубликовано',
            'category': 'Категория:',
        }

    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифры')
        return title


class SubscriptionForm(forms.Form):
    email = forms.EmailField(
        label='Email для рассылки',
        max_length=100,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'example@mail.ru'})
    )
    name = forms.CharField(
        label='Ваше имя',
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя (необязательно)'})
    )


# ФОРМА ДЛЯ КОММЕНТАРИЕВ С КАПЧЕЙ (ЗАДАНИЕ 2)
class CommentForm(forms.ModelForm):
    captcha = CaptchaField(label='Капча')

    class Meta:
        model = Comment
        fields = ['author', 'text']
        widgets = {
            'author': forms.Select(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Ваш комментарий'}),
        }
        labels = {
            'author': 'Автор',
            'text': 'Текст комментария',
        }