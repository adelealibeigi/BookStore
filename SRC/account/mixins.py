from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.utils.decorators import method_decorator

from BookStore import settings


class SuperUserRequiredMixin(object):
    """
    View mixin which requires that the authenticated user is a super user
    (i.e. `is_superuser` is True).
    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            messages.error(
                request, 'شما به این صفحه دسترسی ندارید!')
            return redirect(settings.LOGIN_URL)
        return super(SuperUserRequiredMixin, self).dispatch(request,
            *args, **kwargs)


class StaffRequiredMixin(object):
    """
    View mixin which requires that the authenticated user is a staff member
    (i.e. `is_staff` is True).
    """

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            messages.error(
                request, 'شما به این صفحه دسترسی ندارید!')
            return redirect('accounts:profile')
        return super(StaffRequiredMixin, self).dispatch(request,
            *args, **kwargs)
