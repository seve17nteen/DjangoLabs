from django.urls import path
from .views import *

app_name = 'news'

urlpatterns = [
    path('', HomeNews.as_view(), name='home'),
    path('test/', test, name='test'),
    path('category/<int:category_id>/', NewsByCategory.as_view(), name='category'),
    path('news/<int:pk>/', ViewNews.as_view(), name='view_news'),
    path('news/add-news/', CreateNews.as_view(), name='add_news'),
    path('search/', SearchNews.as_view(), name='search'),  # ← НОВЫЙ МАРШРУТ ДЛЯ ПОИСКА
]