from django.urls import path

from apps.accounts.views import IndexView, AccountsListView, AccountsDetailView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('accounts/', AccountsListView.as_view(), name='accounts'),
    path('accounts/<str:slug>', AccountsDetailView.as_view(), name='account_detail'),
]
