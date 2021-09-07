from django.contrib import admin
from .models import *


# Register your models here.


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'valid_from', 'valid_to', 'amount', 'active')
    list_filter = ('active', 'valid_from', 'valid_to',)
    search_fields = ('code',)


@admin.register(CashDiscount)
class CashDiscountAdmin(admin.ModelAdmin):
    list_display = ('code', 'amount', 'active')
    list_filter = ('active',)
    search_fields = ('code',)


@admin.register(PercentageDiscount)
class PercentageDiscountAdmin(admin.ModelAdmin):
    list_display = ('code', 'amount', 'active')
    list_filter = ('active',)
    search_fields = ('code',)
