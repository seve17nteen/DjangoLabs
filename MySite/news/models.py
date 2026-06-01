from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Наименование категории')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        # Исправлено: добавлено пространство имен 'news:' и правильное имя маршрута
        return reverse('news:category', kwargs={'category_id': self.pk})  # ← для категории


class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    content = models.TextField(blank=True, verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, verbose_name='Категория')

    def get_absolute_url(self):
        # Исправлено: kwargs={'pk': self.pk} (т.к. в DetailView используется pk)
        return reverse('news:view_news', kwargs={'pk': self.pk})  # ← для новости

    def my_func(self):
        return "Последние новости"

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['created_at', ]