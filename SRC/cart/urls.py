from django.urls import path
from .views import *

app_name = 'cart'
urlpatterns = [
    path('', detail, name='cart_detail'),
    path('add/<int:product_id>', cart_add, name='cart_add'),
    path('add_one/<int:product_id>', cart_add_one, name='cart_add_one'),
    path('remove_one/<int:product_id>', cart_remove_one, name='cart_remove_one'),
    path('remove/<int:product_id>', cart_remove, name='cart_remove'),
]