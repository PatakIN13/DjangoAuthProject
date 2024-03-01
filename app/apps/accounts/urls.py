from django.urls import path

from apps.accounts.views import (
    AccountsListView,
    AccountsDetailView,
    AccountsUpdateView,
    AccountsRegisterView,
    AccountsLoginView,
    AccountsLogoutView,
    AccountsPasswordChangeView,
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
]
