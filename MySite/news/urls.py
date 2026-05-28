from django.urls import path
from .views import *

app_name = 'news'

urlpatterns = [
    path('', index, name='home'),
    path('test/', test, name='test'),
    path('category/<int:category_id>/', get_category, name='category'),
]