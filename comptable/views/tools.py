from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse_lazy


def logout_required(function=None, redirect_url=None):
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
        login_url=reverse_lazy(redirect_url) if redirect_url else reverse_lazy('home'),
    )

    if function:
        return actual_decorator(function)
    return actual_decorator


def is_staff(user):
    return user.is_authenticated and user.is_staff
