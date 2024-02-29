from django.views.generic import TemplateView, ListView, DetailView, UpdateView
from django.urls import reverse_lazy

from apps.accounts.form import AccountsUpdateForm
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


class AccountsUpdateView(UpdateView):
    model = Accounts
    form_class = AccountsUpdateForm
    template_name = 'accounts/account_update.html'
    context_object_name = 'account'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование профиля: ' + self.object.username
        if self.request.POST:
            context['account_form'] = AccountsUpdateForm(self.request.POST, instance=self.object)
        else:
            context['account_form'] = AccountsUpdateForm(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        account_form = context['account_form']
        if account_form.is_valid():
            account_form.save()
        else:
            context.update({'account_form': account_form})
            return self.render_to_response(context)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('account_detail', kwargs={'slug': self.object.slug})
