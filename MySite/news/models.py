from django.db import models
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Наименование категории')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:category', kwargs={'category_id': self.pk})


class News(models.Model):
    title = models.CharField(max_length=150, verbose_name='Наименование')
    content = models.TextField(blank=True, verbose_name='Контент')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    photo = models.ImageField(upload_to='photos/%Y/%m/%d', verbose_name='Фото', blank=True)
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, verbose_name='Категория', related_name='get_news')
    views = models.IntegerField(default=0, verbose_name='Просмотры')

    def get_absolute_url(self):
        return reverse('news:view_news', kwargs={'pk': self.pk})

    def my_func(self):
        return "Последние новости"

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']  # сортировка от новых к старым


#НОВЫЕ МОДЕЛИ ДЛЯ 13 ЛАБОРАТОРНОЙ

class Author(models.Model):
    """Модель автора комментариев"""
    name = models.CharField(max_length=100, verbose_name='Имя автора')
    email = models.EmailField(verbose_name='Email', blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Автор'
        verbose_name_plural = 'Авторы'
        ordering = ['name']


class Comment(models.Model):
    """Модель комментария к новости"""
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='comments', verbose_name='Автор')
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments', verbose_name='Новость')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name='Ответ на комментарий')
    text = models.TextField(verbose_name='Текст комментария')
    rating = models.IntegerField(default=0, verbose_name='Рейтинг')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'Комментарий от {self.author.name} к "{self.news.title[:30]}"'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']