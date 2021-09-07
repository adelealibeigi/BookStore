from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):
    mobile_number = models.CharField(max_length=20, unique=True, verbose_name='شماره تماس', null=True, blank=True)
    email = models.EmailField(unique=True, verbose_name='ایمیل')


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=' صاحب آدرس')
    state = models.CharField(max_length=40, verbose_name='استان')
    city = models.CharField(max_length=40, verbose_name='شهر')
    detail_address = models.TextField(max_length=500, verbose_name='جزییات آدرس')
    code = models.IntegerField(verbose_name='کد پستی',null=True)
    phone_number = models.IntegerField(null=True,verbose_name='شماره تماس')

    class Meta:
        ordering = ['state']
        verbose_name = 'آدرس'
        verbose_name_plural = 'آدرس ها'

    def __str__(self):
        return f'{self.user.username} {self.id}'
