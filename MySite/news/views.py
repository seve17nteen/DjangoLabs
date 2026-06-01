from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.db import models
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import News, Category, Comment
from .forms import NewsForm, SubscriptionForm, ContactForm, CommentForm
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
        self.query = self.request.GET.get('q', '')
        if self.query:
            return News.objects.filter(title__icontains=self.query, is_published=True)
        return News.objects.none()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Результаты поиска'
        context['query'] = self.query
        return context


def test(request):
    objects = ["john1", "paul2", "george3", "ringo4", "john5", "paul6", "george7"]
    paginator = Paginator(objects, 2)
    page_num = request.GET.get('page', 1)
    page_objects = paginator.get_page(page_num)
    return render(request, 'news/test.html', {'page_obj': page_objects})


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            email = form.cleaned_data['email']
            message = form.cleaned_data['content']

            try:
                send_mail(
                    subject=f'Обратная связь: {subject}',
                    message=f'От: {email}\n\n{message}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.CONTACT_EMAIL],
                    fail_silently=False,
                )
                messages.success(request, 'Ваше сообщение отправлено!')
                return redirect('news:contact')
            except Exception as e:
                messages.error(request, f'Ошибка отправки: {e}')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        form = ContactForm()

    return render(request, 'news/contact.html', {'form': form})


# ЗАДАНИЕ 2: ДОБАВЛЕНИЕ КОММЕНТАРИЯ С КАПЧЕЙ
def add_comment(request, news_id):
    news = get_object_or_404(News, pk=news_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.news = news
            comment.save()
            messages.success(request, 'Комментарий добавлен!')
            return redirect('news:view_news', pk=news_id)
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме')
    else:
        form = CommentForm()

    return render(request, 'news/add_comment.html', {'form': form, 'news': news})