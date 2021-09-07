from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Address
# Register your models here.


admin.site.site_header = 'فروشگاه کتاب'

UserAdmin.fieldsets[1][1]['fields'] = (
    'first_name', 'last_name', 'email','mobile_number',
)

UserAdmin.list_display += ('is_superuser',)
admin.site.register(User, UserAdmin)
admin.site.register(Address)


# @admin.register(User,UserAdmin)
# class CustomerAdmin(admin.ModelAdmin):
#     def get_queryset(self,request):
#         return User.objects.filter(is_staff=False)
