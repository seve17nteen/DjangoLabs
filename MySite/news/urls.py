from django.urls import path
from .views import *

app_name = 'news'

urlpatterns = [
    path('', index, name='home'),
    path('test/', test, name='test'),
    path('category/<int:category_id>/', get_category, name='category'),
    path('news/<int:news_id>/', view_news, name='view_news'),
]