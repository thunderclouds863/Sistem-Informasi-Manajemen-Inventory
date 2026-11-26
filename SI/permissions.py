from functools import wraps

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden


def is_admin_user(user):
    return bool(
        user and user.is_authenticated and (
            user.is_admin or user.is_staff or user.is_superuser
        )
    )


def admin_required(view_func):
    @login_required(login_url='login')
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not is_admin_user(request.user):
            return HttpResponseForbidden('Administrator access is required for this action.')
        return view_func(request, *args, **kwargs)

    return _wrapped
