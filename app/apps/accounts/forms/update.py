from django.contrib.auth.forms import SetPasswordForm
from django import forms

from apps.accounts.models import Accounts


class AccountsUpdateForm(forms.ModelForm):
    class Meta:
        model = Accounts
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "bio",
            "birth_date",
            "avatar",
            "phone",
            "address",
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {"class": "form-control", "autocomplete": "off"}
            )

    def clean_email(self):
        email = self.cleaned_data.get("email")
        username = self.cleaned_data.get("username")
        if (
            email
            and Accounts.objects.filter(email=email).exclude(username=username).exists()
        ):
            raise forms.ValidationError("Email используется другим пользователем")
        return email


class AccountsPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {"class": "form-control", "autocomplete": "off"}
            )
