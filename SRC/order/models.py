from django.db import models
from django.conf import settings
from product.models import Book
from coupons.models import Coupon
from account.models import Address


# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders'
        , verbose_name='کاربر')

    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='کوپن')
    created = models.DateTimeField(auto_now_add=True, verbose_name='زمان ایجاد')
    updated = models.DateTimeField(auto_now=True, verbose_name='زمان اپدیت')
    address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name='order_address', blank=True, null=True)

    class Meta:
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش ها'

    @property
    def get_total_cost(self):
        total = sum(item.get_cost() for item in self.items.all())
        if self.coupon:
            coupon_amount = (self.coupon.amount / 100) * total
            f_total = int(total - coupon_amount)
            if f_total < total:
                return f_total
        return total

    def __str__(self):
        return f'{self.user}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items', verbose_name='سفارش')
    product = models.ForeignKey(Book, on_delete=models.PROTECT, related_name='order_items', verbose_name='محصول')
    price = models.IntegerField(verbose_name="قیمت")
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد')
    date_added = models.DateTimeField(auto_now_add=True)

    def get_cost(self):
        return self.price * self.quantity

    def __str__(self):
        return f'{self.product.title}'
