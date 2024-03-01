from django.contrib.auth.views import LogoutView, LoginView, PasswordChangeView
from django.views.generic import TemplateView, ListView, DetailView, UpdateView, CreateView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from apps.accounts.forms.update import AccountsUpdateForm, AccountsPasswordForm
from apps.accounts.forms.register import AccountsRegisterForm
from apps.accounts.forms.login import AccountsLoginForm

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
    paginate_by = 5

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
        context['title'] = 'Профиль пользователя: ' + self.object.email
        return context


class AccountsUpdateView(UpdateView):
    model = Accounts
    form_class = AccountsUpdateForm
    template_name = 'accounts/account_update.html'
    context_object_name = 'account'
    success_message = 'Профиль успешно изменен'

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование профиля: ' + self.object.email
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


class AccountsPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    form_class = AccountsPasswordForm
    template_name = 'accounts/account_password_change.html'
    success_message = 'Пароль успешно изменен'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменение пароля: ' + self.request.user.email
        return context

    def get_success_url(self):
        return reverse_lazy('account_detail', kwargs={'slug': self.request.user.slug})


class AccountsRegisterView(SuccessMessageMixin, CreateView):
    form_class = AccountsRegisterForm
    template_name = 'accounts/account_register.html'
    success_url = reverse_lazy('login')
    success_message = 'Пользователь успешно зарегистрирован, теперь вы можете авторизоваться'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context


class AccountsLoginView(SuccessMessageMixin, LoginView):
    form_class = AccountsLoginForm
    template_name = 'accounts/account_login.html'
    success_message = 'Вы успешно авторизованы'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация пользователя'
        return context

    def get_success_url(self):
        return reverse_lazy('account_detail', kwargs={'slug': self.request.user.slug})


class AccountsLogoutView(LogoutView):
    next_page = 'login'
