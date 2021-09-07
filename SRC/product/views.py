from django.shortcuts import render, get_object_or_404
from .models import Category, Book
from django.contrib import messages
from django.http import JsonResponse


# Create your views here.


def home(request, slug=None):

    products = Book.objects.filter(available=True)
    categories = Category.objects.all()
    if slug:
        category = get_object_or_404(Category, slug=slug)
        products = products.filter(category=category)
    return render(request, 'index.html', {'products': products, 'categories': categories})


def product_detail(request, slug):
    product = get_object_or_404(Book, slug=slug)

    if product.inventory == 0:
        messages.error(request,f'!موجود نیست')

    return render(request, 'product/product_detail.html', {'product': product})


def search_result(request):
    if request.is_ajax():
        res = None
        series = request.POST.get('series')
        query_set = Book.objects.filter(
            title__istartswith=series) | Book.objects.filter(author__istartswith=series)

        if len(query_set) > 0 and len(series) > 0:
            data = []
            for book in query_set:
                item = {
                    'slug': book.slug,
                    'title': book.title,
                    'author': book.author,
                }
                data.append(item)
            res = data
        else:
            res = '!کتابی یافت نشد'
        return JsonResponse({'data': res})
    return JsonResponse()

