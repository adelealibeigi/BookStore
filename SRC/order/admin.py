from django.contrib import admin
from .models import *


# Register your models here.


class OrderItemInLine(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('user', 'coupon', 'created', 'get_total_cost')
    inlines = (OrderItemInLine,)
