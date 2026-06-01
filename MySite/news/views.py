from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db import models
from .models import News, Category
from .forms import NewsForm, SubscriptionForm
from .utils import MyMixin, PopularNewsMixin, ActiveLinkMixin


class HomeNews(MyMixin, PopularNewsMixin, ActiveLinkMixin, ListView):
    model = News
    template_name = 'news/home_news_list.html'
    context_object_name = 'news'
    mixin_prop = 'hello world'
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_prop()
        context['popular_news'] = self.get_popular_news()
        context['active_home'] = 'active'
        return context

    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(MyMixin, ListView):
    model = News
    template_name = 'news/category.html'
    context_object_name = 'news'
    allow_empty = False
    paginate_by = 6

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = get_object_or_404(Category, pk=self.kwargs['category_id'])
        context['title'] = category.title
        context['category'] = category
        return context

    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')


class ViewNews(DetailView):
    model = News
    context_object_name = 'news_item'
    template_name = 'news/view_news.html'


class CreateNews(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = NewsForm
    template_name = 'news/add_news.html'
    success_url = reverse_lazy('news:home')
    permission_required = 'news.add_news'
    login_url = '/admin/'


class SearchNews(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'news'
    allow_empty = True
    paginate_by = 2

    def get_queryset(self):
        # Сохраняем query как атрибут класса для использования в get_context_data
        self.query = self.request.GET.get('q', '')
        if self.query:
            return News.objects.filter(title__icontains=self.query, is_published=True)
        return News.objects.none()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Результаты поиска'
        context['query'] = self.query  # Используем сохранённый атрибут
        return context


def test(request):
    objects = ["john1", "paul2", "george3", "ringo4", "john5", "paul6", "george7"]
    paginator = Paginator(objects, 2)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)
    return render(request, 'news/test.html', {'page_obj': page_objects})