from django.urls import path
from .views import *
from coupons.views import coupon_apply

app_name = 'order'
urlpatterns = [
    path('create/', order_create, name='order_create'),
    path('<int:order_id>/', order_detail, name='order_detail'),
    path('apply/<int:order_id>/', coupon_apply, name='coupon_apply'),
    path('order_list/', order_list, name='order_list'),

]
