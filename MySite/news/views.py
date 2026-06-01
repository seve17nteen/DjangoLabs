from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
# Create your views here.
from django.http import HttpResponse
from .models import News, Category
from .forms import NewsForm, SubscriptionForm
from django.db import models

class HomeNews(ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True)


class NewsByCategory(ListView):
    model = News
    template_name = 'news/category.html'
    context_object_name = 'news'
    allow_empty = False

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(pk=self.kwargs['category_id'])
        context['title'] = category
        context['category'] = category
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True)


class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'
    template_name = 'news/view_news.html'


class CreateNews(CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    success_url = reverse_lazy('news:home')


# ===== НОВЫЙ КЛАСС ДЛЯ ПОИСКА (ВАРИАНТ 13) =====
class SearchNews(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'news'
    allow_empty = True

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        if query:
            return News.objects.filter(title__icontains=query, is_published=True)
        return News.objects.none()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Результаты поиска'
        context['query'] = self.request.GET.get('q', '')
        return context


class SearchNews(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'news'
    allow_empty = True

    def get_queryset(self):
        query = self.request.GET.get('q', '')

        if query:
            # Приводим запрос к нижнему регистру
            query_lower = query.lower()

            # Фильтруем, также приводя заголовок к нижнему регистру
            return News.objects.filter(
                models.Q(title__icontains=query_lower) |
                models.Q(title__icontains=query.upper()),
                is_published=True
            )
        return News.objects.none()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Результаты поиска'
        context['query'] = self.request.GET.get('q', '')
        return context

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Результаты поиска'
        context['query'] = self.request.GET.get('q', '')
        print(f"Контекст: query={context['query']}, news count={context['news'].count()}")  # ← ОТЛАДКА
        return context

def test(request):
    return HttpResponse('<h1>Тестовая страница</h1>')


# ===== СТАРЫЕ ФУНКЦИИ (ЗАКОММЕНТИРОВАНЫ) =====
'''
def index(request):
    news = News.objects.all()
    context = {
        'news': news,
        'title': 'Список новостей',
    }
    return render(request, template_name='news/index.html', context=context)

def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    return render(request, 'news/category.html', {'news': news, 'category': category})

def view_news(request, news_id):
    news_item = get_object_or_404(News, pk=news_id)
    return render(request, 'news/view_news.html', {'news_item': news_item})

def add_news(request):
    news_form = NewsForm()
    sub_form = SubscriptionForm()
    sub_success = None

    if request.method == "POST":
        if 'add_news' in request.POST:
            news_form = NewsForm(request.POST, request.FILES)
            if news_form.is_valid():
                news = news_form.save()
                return redirect('news:view_news', news_id=news.pk)

        elif 'subscribe' in request.POST:
            sub_form = SubscriptionForm(request.POST)
            if sub_form.is_valid():
                sub_success = 'Вы успешно подписались на рассылку!'

    return render(request, 'news/add_news.html', {
        'news_form': news_form,
        'sub_form': sub_form,
        'sub_success': sub_success,
    })
'''