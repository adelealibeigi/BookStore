from django.shortcuts import render, get_object_or_404, redirect
from account.models import Address
from .cart import Cart
from product.models import Book
from django.views.decorators.http import require_POST
from django.contrib import messages

# Create your views here.


def detail(request):
    cart = Cart(request)
    item_quantity = [i for i, item in enumerate(cart)]
    if not item_quantity:
        item_quantity = 'empty'

    addresses = None
    if request.user.is_authenticated:
        addresses = Address.objects.filter(user=request.user)

    if not addresses:
        messages.warning(request, f'!آدرسی وجود ندارد')
    for item in cart:
        book = Book.objects.get(slug=item['slug'])

        if item['quantity'] > book.inventory:
            messages.error(request, f'!'
                                    f' کتاب {book.title} '
                                    f' {item["quantity"]} '
                                    f' عدد موجود نیست ')
    context = {
        'addresses': addresses,
        'cart': cart,
        'item_quantity': item_quantity,
    }
    return render(request, 'cart/detail.html', context)


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Book, id=product_id)

    cart.add(product=product)
    return redirect('cart:cart_detail')


def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Book, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')


def cart_add_one(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Book, id=product_id)

    cart.add_one(product=product)
    return redirect('cart:cart_detail')


def cart_remove_one(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Book, id=product_id)

    cart.remove_one(product=product)
    return redirect('cart:cart_detail')