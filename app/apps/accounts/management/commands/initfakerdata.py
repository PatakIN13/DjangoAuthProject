from django.core.management.base import BaseCommand
from apps.accounts.models import Accounts
from faker import Faker


class Command(BaseCommand):
    def handle(self, *args, **options):
        fake = Faker("ru_RU")

        for _ in range(10):
            Accounts.objects.create(
                username=fake.user_name(),
                email=fake.email(),
                password=fake.password(),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                bio=fake.text(),
            )
