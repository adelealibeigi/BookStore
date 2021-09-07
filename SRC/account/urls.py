from django.contrib.auth import views
from django.urls import path
from .views import (
    BookList, BookCreate, BookUpdate, BookDelete,
    Profile,
    CategoryList, CategoryCreate, CategoryDelete, CategoryUpdate,
    Report,AddressView,AddressDelete,AddressUpdate
)

app_name = 'accounts'

urlpatterns = [
    path("", BookList.as_view(), name='home'),
    path("book/create", BookCreate.as_view(), name='book_create'),
    path("book/update/<int:pk>", BookUpdate.as_view(), name='book_update'),
    path("book/delete/<int:pk>", BookDelete.as_view(), name='book_delete'),

    path("categories", CategoryList.as_view(), name='category_list'),
    path("category/create", CategoryCreate.as_view(), name='category_create'),
    path("category/update/<int:pk>", CategoryUpdate.as_view(), name='category_update'),
    path("category/delete/<int:pk>", CategoryDelete.as_view(), name='category_delete'),

    path("profile/", Profile.as_view(), name='profile'),

    path('my-address/', AddressView.as_view(), name='my_address'),
    path('<pk>/update', AddressUpdate.as_view(), name='update_address'),
    path('<pk>/delete/', AddressDelete.as_view(), name='delete_address'),
    path('report', Report.as_view(), name='report')
]
