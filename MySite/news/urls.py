from django.urls import path
from django.views.decorators.cache import cache_page
from .views import *

app_name = 'news'

urlpatterns = [
    path('', HomeNews.as_view(), name='home'),
    path('contact/', contact, name='contact'),
    path('category/<int:category_id>/', cache_page(25)(NewsByCategory.as_view()), name='category'),
    path('news/<int:pk>/', ViewNews.as_view(), name='view_news'),
    path('news/add-news/', CreateNews.as_view(), name='add_news'),
    path('search/', SearchNews.as_view(), name='search'),
    path('add-comment/<int:news_id>/', add_comment, name='add_comment'),
]