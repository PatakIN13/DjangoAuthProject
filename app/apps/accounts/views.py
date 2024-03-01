from django.conf.global_settings import EMAIL_HOST_USER
from django.contrib.auth.views import (
    LogoutView,
    LoginView,
    PasswordChangeView,
    PasswordResetView,
    PasswordResetConfirmView,
)
from django.views import View
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    UpdateView,
    CreateView,
)
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib.auth import login

from apps.accounts.forms.password import (
    AccountsForgotPasswordForm,
    AccountsSetNewPasswordForm,
)
from apps.accounts.forms.update import AccountsUpdateForm, AccountsPasswordForm
from apps.accounts.forms.register import AccountsRegisterForm
from apps.accounts.forms.login import AccountsLoginForm
from apps.accounts.mixins import AccountsIsNotAuthenticatedMixin

from apps.accounts.models import Accounts


# Create your views here.


class IndexView(TemplateView):
    template_name = "index.html"
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Главная страница"
        return context


class AccountsListView(ListView):
    model = Accounts
    template_name = "accounts/accounts.html"
    context_object_name = "accounts"
    ordering = ("-date_joined",)
    paginate_by = 5

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Пользователи"
        return context


class AccountsDetailView(DetailView):
    model = Accounts
    template_name = "accounts/account_detail.html"
    context_object_name = "account"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Профиль пользователя: " + self.object.email
        return context


class AccountsUpdateView(UpdateView):
    model = Accounts
    form_class = AccountsUpdateForm
    template_name = "accounts/account_update.html"
    context_object_name = "account"
    success_message = "Профиль успешно изменен"

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Редактирование профиля: " + self.object.email
        if self.request.POST:
            context["account_form"] = AccountsUpdateForm(
                self.request.POST, instance=self.object
            )
        else:
            context["account_form"] = AccountsUpdateForm(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        account_form = context["account_form"]
        if account_form.is_valid():
            account_form.save()
        else:
            context.update({"account_form": account_form})
            return self.render_to_response(context)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("account_detail", kwargs={"slug": self.object.slug})


class AccountsPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    form_class = AccountsPasswordForm
    template_name = "accounts/account_password_change.html"
    success_message = "Пароль успешно изменен"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Изменение пароля: " + self.request.user.email
        return context

    def get_success_url(self):
        return reverse_lazy("account_detail", kwargs={"slug": self.request.user.slug})


class AccountsRegisterView(AccountsIsNotAuthenticatedMixin, CreateView):
    form_class = AccountsRegisterForm
    template_name = "accounts/account_register.html"
    success_url = reverse_lazy("login")
    success_message = (
        "Пользователь успешно зарегистрирован, теперь вы можете авторизоваться"
    )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Регистрация на сайте"
        return context

    def form_valid(self, form):
        account = form.save(commit=False)
        account.is_active = False
        account.save()

        token = default_token_generator.make_token(account)
        uid = account.pk
        print(uid, token)
        activation_url = reverse_lazy(
            "confirm_email", kwargs={"uidb64": uid, "token": token}
        )
        current_site = Site.objects.get_current().domain
        send_mail(
            "Подтверждение email",
            f"Для подтверждения email перейдите по ссылке: http://{current_site}{activation_url}",
            EMAIL_HOST_USER,
            [account.email],
            fail_silently=False,
        )
        return redirect("email_confirmation_sent")


class AccountsLoginView(SuccessMessageMixin, LoginView):
    form_class = AccountsLoginForm
    template_name = "accounts/account_login.html"
    success_message = "Вы успешно авторизованы"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Авторизация пользователя"
        return context

    def get_success_url(self):
        return reverse_lazy("account_detail", kwargs={"slug": self.request.user.slug})


class AccountsLogoutView(LogoutView):
    next_page = "login"


class AccountsForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    form_class = AccountsForgotPasswordForm
    template_name = "accounts/account_forgot_password.html"
    success_url = reverse_lazy("login")
    success_message = "Ссылка для восстановления пароля отправлена на ваш email"
    subject_template_name = "components/email/forgot_password_subject.txt"
    email_template_name = "components/email/forgot_password_email.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Восстановление пароля"
        return context


class AccountsSetNewPasswordConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    form_class = AccountsSetNewPasswordForm
    template_name = "accounts/account_set_new_password.html"
    success_url = reverse_lazy("login")
    success_message = "Пароль успешно изменен. Можете авторизоваться на сайте."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Изменение пароля"
        return context


class AccountsConfirmEmailView(View):
    def get(self, request, uidb64, token):
        try:
            accounts = Accounts.objects.get(pk=uidb64)
        except (TypeError, ValueError, OverflowError):
            accounts = None
        print(accounts)
        if accounts is not None and default_token_generator.check_token(
            accounts, token
        ):
            accounts.is_active = True
            accounts.save()
            login(request, accounts)
            return redirect("email_confirmed")
        else:
            return redirect("email_confirmation_failed")


class EmailConfirmationSentView(TemplateView):
    template_name = "accounts/email/email_confirmation_sent.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Письмо активации отправлено"
        return context


class EmailConfirmedView(TemplateView):
    template_name = "accounts/email/email_confirmed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Ваш электронный адрес активирован"
        return context


class EmailConfirmationFailedView(TemplateView):
    template_name = "accounts/email/email_confirmation_failed.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Ваш электронный адрес не активирован"
        return context
