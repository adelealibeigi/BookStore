from django.contrib import admin
from .models import Category, Book


# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',)
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'inventory', 'thumbnail_tag', 'category_to_str')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('category', 'created')
    list_editable = ('price', 'inventory')
