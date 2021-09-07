from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect, HttpResponse
from django.contrib.auth.decorators import login_required

from account.models import Address
from .models import Order, OrderItem
from cart.cart import Cart
from coupons.forms import CouponForm


from product.models import Book
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


@login_required()
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    form = CouponForm()
    return render(request, 'order/order.html', {'order': order, 'form': form})


# ثبت سفارش از سبد خرید
@login_required()
def order_create(request):
    cart = Cart(request)
    address = Address.objects.get(id=request.POST.get('my_address'))
    order = Order.objects.create(user=request.user)
    order.address = address
    order.save()

    for item in cart:
        obj = Book.objects.get(id=item['id'])
        if item['quantity'] <= obj.inventory:
            obj.inventory = obj.inventory - item['quantity']
            obj.save()
            OrderItem.objects.create(order=order, product=item['product'], price=item['price'],
                quantity=item['quantity'])

            cart.clear()

    return redirect('order:order_detail', order.id)


@login_required()
def order_list(request):
    orders = Order.objects.filter(user=request.user)

    return render(request, 'registration/order_list.html', {'orders': orders})
