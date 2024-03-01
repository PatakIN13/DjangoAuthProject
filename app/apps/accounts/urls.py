from django.urls import path

from apps.accounts.views import (
    AccountsListView,
    AccountsDetailView,
    AccountsUpdateView,
    AccountsRegisterView,
    AccountsLoginView,
    AccountsLogoutView,
    AccountsPasswordChangeView,
    AccountsForgotPasswordView,
    AccountsSetNewPasswordConfirmView,
    AccountsConfirmEmailView,
    EmailConfirmationSentView,
    EmailConfirmedView,
    EmailConfirmationFailedView,
)


urlpatterns = [
    path("", AccountsListView.as_view(), name="accounts"),
    path("accounts/update", AccountsUpdateView.as_view(), name="account_update"),
    path(
        "accounts/password_change",
        AccountsPasswordChangeView.as_view(),
        name="account_password_change",
    ),
    path("accounts/<str:slug>", AccountsDetailView.as_view(), name="account_detail"),
    path("login/", AccountsLoginView.as_view(), name="login"),
    path("logout/", AccountsLogoutView.as_view(), name="logout"),
    path("register/", AccountsRegisterView.as_view(), name="register"),
    path(
        "email-confirmation-sent/",
        EmailConfirmationSentView.as_view(),
        name="email_confirmation_sent",
    ),
    path(
        "confirm-email/<str:uidb64>/<str:token>/",
        AccountsConfirmEmailView.as_view(),
        name="confirm_email",
    ),
    path("email-confirmed/", EmailConfirmedView.as_view(), name="email_confirmed"),
    path(
        "confirm-email-failed/",
        EmailConfirmationFailedView.as_view(),
        name="email_confirmation_failed",
    ),
    path(
        "forgot_password/", AccountsForgotPasswordView.as_view(), name="forgot_password"
    ),
    path(
        "set_new_password/<uidb64>/<token>/",
        AccountsSetNewPasswordConfirmView.as_view(),
        name="set_new_password",
    ),
]
