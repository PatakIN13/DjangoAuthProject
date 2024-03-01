from django.urls import path

from apps.accounts.views import IndexView, AccountsListView, AccountsDetailView, AccountsUpdateView, AccountRegisterView, AccountLoginView, AccountLogoutView, AccountPasswordChangeView


urlpatterns = [
    path('', AccountsListView.as_view(), name='accounts'),
    path('accounts/update', AccountsUpdateView.as_view(), name='account_update'),
    path('accounts/password_change', AccountPasswordChangeView.as_view(), name='account_password_change'),
    path('accounts/<str:slug>', AccountsDetailView.as_view(), name='account_detail'),
    path('login/', AccountLoginView.as_view(), name='login'),
    path('logout/', AccountLogoutView.as_view(), name='logout'),
    path('register/', AccountRegisterView.as_view(), name='register'),
]
