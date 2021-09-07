from django.urls import path
from .views import *
from django.views.decorators.csrf import csrf_exempt


app_name = 'product'
urlpatterns = [
    path('', home, name='home'),
    path('category/<slug:slug>', home, name='category_filter'),
    path('<slug:slug>/', product_detail, name='product_detail'),
    path('search', search_result, name='search_result'),
]
