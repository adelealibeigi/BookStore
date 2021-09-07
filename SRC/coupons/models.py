from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='کد')
    valid_from = models.DateTimeField(verbose_name='از زمان')
    valid_to = models.DateTimeField(verbose_name="تا زمان")
    amount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="مقدار")
    active = models.BooleanField(verbose_name='فعال', default=False)

    class Meta:
        verbose_name = 'کوپن'
        verbose_name_plural = 'کوپن ها'

    def __str__(self):
        return self.code


class PercentageDiscount(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='کد')
    amount = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], verbose_name="مقدار")
    active = models.BooleanField(verbose_name='فعال', default=False)

    class Meta:
        verbose_name = 'تخفیف درصدی'
        verbose_name_plural = 'تخفیف های درصدی'

    def __str__(self):
        return self.code


class CashDiscount(models.Model):
    code = models.CharField(max_length=50, unique=True, verbose_name='کد')
    amount = models.PositiveIntegerField(verbose_name="مقدار")
    active = models.BooleanField(verbose_name='فعال', default=False)

    class Meta:
        verbose_name = 'تخفیف نقدی'
        verbose_name_plural = 'تخفیف های نقدی'

    def __str__(self):
        return self.code
