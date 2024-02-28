from django.views.generic import ListView, DetailView

from apps.accounts.models import Accounts


# Create your views here.


class AccountsListView(ListView):
    model = Accounts
    template_name = 'accounts.html'
    context_object_name = 'accounts'
    ordering = ('-date_joined',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Пользователи'
        return context


class AccountsDetailView(DetailView):
    model = Accounts
    template_name = 'account_detail.html'
    context_object_name = 'account'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Профиль пользователя: ' + self.object.username
        return context
