from django.shortcuts import render, get_object_or_404, redirect
# Create your views here.
from django.http import HttpResponse
from .models import News, Category
from .forms import NewsForm, SubscriptionForm  # ИМПОРТИРУЮ ОБЕ ФОРМЫ


def index(request):
    news = News.objects.all()
    context = {
        'news': news,
        'title': 'Список новостей',
    }
    return render(request, template_name='news/index.html', context=context)


def test(request):
    return HttpResponse('<h1>Тестовая страница</h1>')


def get_category(request, category_id):
    news = News.objects.filter(category_id=category_id)
    category = Category.objects.get(pk=category_id)
    return render(request, 'news/category.html', {'news': news, 'category': category})


def view_news(request, news_id):
    news_item = get_object_or_404(News, pk=news_id)
    return render(request, 'news/view_news.html', {'news_item': news_item})


# ПЕРЕПИСАННАЯ ФУНКЦИЯ add_news
def add_news(request):
    # СОЗДАЮ ОБЕ ФОРМЫ
    news_form = NewsForm()
    sub_form = SubscriptionForm()
    sub_success = None

    if request.method == "POST":
        # ПРОВЕРЯЮ, КАКАЯ КНОПКА БЫЛА НАЖАТА
        if 'add_news' in request.POST:
            news_form = NewsForm(request.POST, request.FILES)
            if news_form.is_valid():
                news = news_form.save()
                return redirect('news:view_news', news_id=news.pk)

        elif 'subscribe' in request.POST:
            sub_form = SubscriptionForm(request.POST)
            if sub_form.is_valid():
                # ЗДЕСЬ МОЖНО СОХРАНИТЬ ПОДПИСКУ
                sub_success = 'Вы успешно подписались на рассылку!'

    return render(request, 'news/add_news.html', {
        'news_form': news_form,
        'sub_form': sub_form,
        'sub_success': sub_success,
    })