from django.contrib import admin
from django.contrib.admin import SimpleListFilter
from django.utils.translation import gettext_lazy as _
from datetime import datetime, timedelta
from .models import News, Category, Author, Comment


# ===== ЗАДАНИЕ 1: КАСТОМНЫЙ DateRangeFilter =====
class DateRangeFilter(SimpleListFilter):
    title = _('Диапазон дат')
    parameter_name = 'date_range'

    def lookups(self, request, model_admin):
        return (
            ('today', _('Сегодня')),
            ('week', _('За неделю')),
            ('month', _('За месяц')),
            ('year', _('За год')),
        )

    def queryset(self, request, queryset):
        today = datetime.now().date()
        if self.value() == 'today':
            return queryset.filter(created_at__date=today)
        if self.value() == 'week':
            week_ago = today - timedelta(days=7)
            return queryset.filter(created_at__date__gte=week_ago)
        if self.value() == 'month':
            month_ago = today - timedelta(days=30)
            return queryset.filter(created_at__date__gte=month_ago)
        if self.value() == 'year':
            year_ago = today - timedelta(days=365)
            return queryset.filter(created_at__date__gte=year_ago)
        return queryset


# ===== ЗАДАНИЕ 2 И 3: НАСТРОЙКА ADMIN =====
class NewsAdmin(admin.ModelAdmin):
    # Базовый список полей (должен включать is_published для list_editable)
    list_display = ['id', 'title', 'category', 'views', 'is_published', 'created_at', 'updated_at']
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')

    # ЗАДАНИЕ 1: Добавлен кастомный фильтр DateRangeFilter
    list_filter = ('is_published', 'category', DateRangeFilter)

    # ЗАДАНИЕ 2: autocomplete_fields для ForeignKey
    autocomplete_fields = ['category']

    # Редактируемые поля (должны быть в list_display)
    list_editable = ['is_published']

    list_per_page = 20
    date_hierarchy = 'created_at'
    ordering = ['-created_at']


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'get_news_count')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    ordering = ['title']

    def get_news_count(self, obj):
        return obj.get_news.count()

    get_news_count.short_description = 'Количество новостей'


# Регистрация моделей
admin.site.register(News, NewsAdmin)
admin.site.register(Category, CategoryAdmin)