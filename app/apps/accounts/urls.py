from django.urls import path

from apps.accounts.views import AccountsListView, AccountsDetailView


urlpatterns = [
    path('accounts/', AccountsListView.as_view(), name='accounts'),
    path('accounts/<str:slug>', AccountsDetailView.as_view(), name='account_detail'),
]
