from django.core.management.base import BaseCommand
from apps.accounts.models import Accounts
import os


class Command(BaseCommand):
    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@admin.com")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "P@ssw0rd")

        if not Accounts.objects.filter(email=email).exists():

            Accounts.objects.create_superuser(
                username=username, email=email, password=password
            )
