from django.urls import path

from apps.accounts.views import IndexView, AccountsListView, AccountsDetailView, AccountsUpdateView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('accounts/', AccountsListView.as_view(), name='accounts'),
    path('accounts/update', AccountsUpdateView.as_view(), name='account_update'),
    path('accounts/<str:slug>', AccountsDetailView.as_view(), name='account_detail'),
]
