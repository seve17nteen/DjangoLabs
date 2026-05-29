from django import forms
from django.template.defaultfilters import title

from .models import News, Category
import re
from django.core.exceptions import ValidationError


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


# ДОБАВЛЕНА НОВАЯ ФОРМА ДЛЯ ПОДПИСКИ
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