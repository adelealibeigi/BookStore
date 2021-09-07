from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.shortcuts import render, redirect
from django.views.generic import (ListView, CreateView, UpdateView, DeleteView)

from cart.cart import Cart
from product.models import Book, Category
from .mixins import SuperUserRequiredMixin, StaffRequiredMixin
from django.urls import reverse_lazy
from .models import User, Address
from .forms import ProfileForm, CheckoutForm
from django.contrib.auth.views import LoginView
from django.views.generic.base import View

from django.http import HttpResponse
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage, send_mail
from order.models import Order
from coupons.models import CashDiscount, PercentageDiscount
import jdatetime
from django.urls import reverse
from django.urls import reverse_lazy
from django.views.generic.base import View
from django.views.generic import UpdateView, DeleteView
from django.contrib import messages


class BookList(StaffRequiredMixin, ListView):
    queryset = Book.objects.all()
    template_name = 'registration/home.html'


class BookCreate(StaffRequiredMixin, CreateView):
    model = Book
    fields = [
        'title', 'description', 'category', 'author', 'price', 'cover',
        'slug', 'c_discount', 'p_discount', 'inventory'
    ]
    template_name = 'registration/book_create_update.html'


class BookUpdate(StaffRequiredMixin, UpdateView):
    model = Book
    fields = [
        'title', 'description', 'category', 'author', 'price', 'cover',
        'slug', 'c_discount', 'p_discount', 'inventory'
    ]
    template_name = 'registration/book_create_update.html'


class BookDelete(StaffRequiredMixin, DeleteView):
    model = Book
    template_name = 'registration/book_confirm_delete.html'
    success_url = reverse_lazy('accounts:home')


class CategoryList(StaffRequiredMixin, ListView):
    queryset = Category.objects.all()
    template_name = 'registration/category_list.html'


class CategoryCreate(StaffRequiredMixin, CreateView):
    model = Category
    fields = [
        'title', 'slug'
    ]
    template_name = 'registration/category_create_update.html'


class CategoryUpdate(StaffRequiredMixin, UpdateView):
    model = Category
    fields = [
        'title', 'slug'
    ]
    template_name = 'registration/category_create_update.html'


class CategoryDelete(StaffRequiredMixin, DeleteView):
    model = Category
    template_name = 'registration/category_confirm_delete.html'
    success_url = reverse_lazy('accounts:category_list')


class Profile(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'registration/profile.html'
    form_class = ProfileForm
    success_url = reverse_lazy('accounts:profile')

    def get_object(self, queryset=None):
        return User.objects.get(pk=self.request.user.pk)

    def get_form_kwargs(self):
        kwargs = super(Profile, self).get_form_kwargs()
        kwargs.update({
            'user': self.request.user
        })
        return kwargs


class Login(LoginView):
    def get_success_url(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return reverse_lazy('accounts:home')
        else:
            return reverse_lazy('accounts:profile')


class Register(CreateView):
    form_class = SignupForm
    template_name = 'registration/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'فعال سازی حساب کاربری'
        message = render_to_string('registration/activate_account.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),
        })
        to_email = form.cleaned_data.get('email')

        email_from = settings.EMAIL_HOST_USER
        send_mail(
            mail_subject,
            message,
            email_from,
            [to_email],
            fail_silently=False,
        )
        return HttpResponse("<a href='/login'>ورود</a> لینک به ایمیل شما ارسال شد")


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return HttpResponse('<a href="/login">'
                            'حساب شما با موفقیت فعال شد')
    else:
        return HttpResponse('<a href="/registration">'
                            'لینک منقضی شده است!')


class Report(SuperUserRequiredMixin, View):
    def get(self, *args, **kwargs):
        users = User.objects.all()

        staff_users = (users.filter(is_staff=True) & users.filter(is_superuser=False)).count()
        super_users = users.filter(is_superuser=True).count()
        simple_users = users.filter(is_staff=False).count()

        # c_discounts = CashDiscount.objects.annotate(num_book=Count('discount'))
        # p_discounts = PercentageDiscount.objects.annotate(num_book=Count('discount'))

        # num_discount_book = c_discounts[0].num_book + p_discounts[0].num_book

        num_no_discounts = Book.objects.filter(c_discount=None) & Book.objects.filter(p_discount=None) \
                           | (Book.objects.filter(c_discount__active=False)
                              | Book.objects.filter(p_discount__active=False))
        all_book = Book.objects.all().count()

        orders = Order.objects.all()
        orders_count = orders.count()

        earn = sum(order.get_total_cost for order in orders)
        time = jdatetime.datetime.today
        context = {
            'staff_users': staff_users,
            'super_users': super_users,
            'simple_users': simple_users,

            'num_discount_book': all_book - num_no_discounts.count(),
            'num_no_discounts': num_no_discounts.count(),
            'orders_count': orders_count,
            'earn': earn,
            'time': time

        }

        return render(self.request, 'registration/reports.html', context)


class AddressView(LoginRequiredMixin, View):

    def get(self, *args, **kwargs):
        form = CheckoutForm()
        addresses = Address.objects.filter(user=self.request.user)
        context = {
            'form': form,
            'addresses': addresses,
        }
        return render(self.request, 'registration/my_address.html', context)

    def post(self, *args, **kwargs):
        form = CheckoutForm(self.request.POST or None)

        if form.is_valid():
            state = form.cleaned_data.get('state')
            city = form.cleaned_data.get('city')
            detail_address = form.cleaned_data.get('detail_address')
            code = form.cleaned_data.get('code')
            phone_number = form.cleaned_data.get('phone_number')
            address = Address(
                user=self.request.user,
                state=state,
                city=city,
                detail_address=detail_address,
                code=code,
                phone_number=phone_number,
            )
            address.save()

            return redirect('accounts:my_address')


class AddressUpdate(UpdateView):
    model = Address
    fields = ['state', 'city', 'detail_address', 'code', 'phone_number']
    template_name = 'order/update_address.html'

    def get_success_url(self):
        return reverse('accounts:my_address')


class AddressDelete(DeleteView):
    model = Address
    template_name = 'registration/address_confirm_delete.html'

    def get_success_url(self):
        success_url = reverse_lazy('accounts:my_address')
        return success_url
