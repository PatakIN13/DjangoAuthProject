from django.views.generic import TemplateView, ListView, DetailView

from apps.accounts.models import Accounts


# Create your views here.

class IndexView(TemplateView):
    template_name = 'index.html'
    success_url = '/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        return context


class AccountsListView(ListView):
    model = Accounts
    template_name = 'accounts/accounts.html'
    context_object_name = 'accounts'
    ordering = ('-date_joined',)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Пользователи'
        return context


class AccountsDetailView(DetailView):
    model = Accounts
    template_name = 'accounts/account_detail.html'
    context_object_name = 'account'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Профиль пользователя: ' + self.object.username
        return context
