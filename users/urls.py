from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy

from .forms import TarindoPasswordResetForm, TarindoSetPasswordForm
from .views import (
    approve_account,
    login_page,
    logout_page,
    pending_approvals_page,
    profile_page,
    register_page,
    reject_account,
)

urlpatterns = [
    path('login/', login_page, name='login'),
    path('register/', register_page, name='register'),
    path('logout/', logout_page, name='logout'),
    path('profile/', profile_page, name='profile'),
    path('approvals/', pending_approvals_page, name='pending-approvals'),
    path('approvals/<int:user_id>/approve/', approve_account, name='approve-account'),
    path('approvals/<int:user_id>/reject/', reject_account, name='reject-account'),

    # Password Reset Flow (Django secure single-use token generator)
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            template_name='users/password_reset.html',
            email_template_name='users/password_reset_email.txt',
            subject_template_name='users/password_reset_subject.txt',
            form_class=TarindoPasswordResetForm,
            success_url=reverse_lazy('password_reset_done'),
        ),
        name='password_reset',
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='users/password_reset_done.html',
        ),
        name='password_reset_done',
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='users/password_reset_confirm.html',
            form_class=TarindoSetPasswordForm,
            success_url=reverse_lazy('password_reset_complete'),
        ),
        name='password_reset_confirm',
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='users/password_reset_complete.html',
        ),
        name='password_reset_complete',
    ),
]
