from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from .models import News
from .models import News, Category
def index(request):
    news = News.objects.all()
    categories = Category.objects.all()
    context={
        'news':news,
        'title' : 'Список новостей',
        'categories' : categories,
    }
    return render(request,template_name='news/index.html', context=context)




    '''
    res = '<h1>Список новостей</h1>'
    for item in news:
        res+=f'<div>\n<p>{item.title}</p>\n<p>{item.content}</p>\n</div>\n<hr>'
  #  print(dir(request))
    return HttpResponse(res)
'''
def test(request):
    return HttpResponse('<h1>Тестовая страница</h1>')


def get_category(request, category_id):
    news=News.objects.filter(category_id=category_id)
    categories = Category.objects.all()
    category=Category.objects.get(pk=category_id)
    return render(request, 'news/category.html', {'news': news, 'categories': categories, 'category': category})
