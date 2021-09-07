from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.utils import timezone
from .forms import CouponForm
from .models import Coupon
from django.contrib import messages
from order.models import Order

# Create your views here.


@require_POST
def coupon_apply(request, order_id):
    now = timezone.now()
    form = CouponForm(request.POST)
    if form.is_valid():
        code = form.cleaned_data['code']
        try:
            coupon = Coupon.objects.get(code__iexact=code, valid_from__lte=now, valid_to__gte=now, active=True)
        except Coupon.DoesNotExist:
            messages.error(request, '!این کوپن اعتبار ندارد', 'danger')
            return redirect('order:order_detail', order_id)
        order = Order.objects.get(id=order_id)

        order.coupon = coupon
        order.save()
    return redirect('order:order_detail', order_id)
