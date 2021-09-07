from django.db import models
from django.urls import reverse
from coupons.models import CashDiscount, PercentageDiscount
from django.utils.html import format_html


class Category(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name="عنوان")
    slug = models.SlugField(max_length=200, db_index=True, unique=True, allow_unicode=True, verbose_name='اسلاگ')

    class Meta:
        ordering = ['title']
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def get_absolute_url(self):
        return reverse('accounts:category_list')

    def __str__(self):
        return self.title


class Book(models.Model):
    title = models.CharField(max_length=200, db_index=True, verbose_name='عنوان')
    description = models.TextField(blank=True, verbose_name='توضیحات')
    category = models.ManyToManyField(Category, related_name='categories', verbose_name='دسته بندی')
    author = models.CharField(max_length=200, verbose_name='نویسنده کتاب')
    price = models.PositiveIntegerField(verbose_name='قیمت')
    cover = models.ImageField(upload_to='cover/products/', null=True, blank=True, verbose_name='کاور')
    available = models.BooleanField(default=True, verbose_name='موجودی انبار')
    created = models.DateField(auto_now_add=True, verbose_name='تاریخ ثبت کتاب')
    updated = models.DateTimeField(auto_now=True, verbose_name='تاریخ اپدیت کتاب')
    slug = models.SlugField(max_length=200, db_index=True, allow_unicode=True, verbose_name='اسلاگ')
    c_discount = models.ForeignKey(CashDiscount, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='discount', verbose_name='تخفیف نقدی')
    p_discount = models.ForeignKey(PercentageDiscount, blank=True, null=True, on_delete=models.SET_NULL,
        related_name='discount', verbose_name='تخفیف درصدی')
    inventory = models.PositiveIntegerField(null=True, blank=True, verbose_name='موجودی انبار ')

    class Meta:
        ordering = ['title']
        verbose_name = 'کتاب'
        verbose_name_plural = 'کتاب ها'
        index_together = [
            ['id', 'slug']
        ]

    @property
    def final_price(self):
        if self.c_discount and self.c_discount.active:
            return self.price - self.c_discount.amount
        elif self.p_discount and self.p_discount.active:
            discount_amount = (self.p_discount.amount / 100) * self.price
            return int(self.price - discount_amount)
        return self.price

    def get_absolute_url(self):
        return reverse('accounts:home')

    def thumbnail_tag(self):
        return format_html('<img width="100" height="100" style="border-radius:5px" src="{}">'.format(self.cover.url))

    thumbnail_tag.short_description = 'عکس'

    def category_to_str(self):
        return ','.join([category.title for category in self.category.all()])

    category_to_str.short_description = 'دسته بندی'

    def __str__(self):
        return self.title
