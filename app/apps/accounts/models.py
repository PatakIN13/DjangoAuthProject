# Create your models here.
import uuid
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser, PermissionsMixin

from apps.accounts.utils import unique_slugify


# Create your models here.


class Accounts(AbstractUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=150, verbose_name='Логин', unique=True)
    slug = models.SlugField(max_length=150, unique=True, blank=True, verbose_name='URL')
    email = models.EmailField(unique=True, verbose_name='Email')
    first_name = models.CharField(max_length=150, verbose_name='Имя')
    last_name = models.CharField(max_length=150, verbose_name='Фамилия')
    bio = models.TextField(max_length=500, blank=True, verbose_name='Информация о себе')
    birth_date = models.DateField(null=True, blank=True, verbose_name='Дата рождения')
    phone = models.CharField(max_length=20, blank=True, verbose_name='Телефон')
    address = models.CharField(max_length=255, blank=True, verbose_name='Адрес')
    avatar = models.ImageField(
        verbose_name='Аватар',
        upload_to='images/avatars/%Y/%m/%d/',
        blank=True,
        validators=[FileExtensionValidator(allowed_extensions=('png', 'jpg', 'jpeg'))])
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='Дата регистрации')
    last_login = models.DateTimeField(auto_now=True, verbose_name='Последний вход')
    is_active = models.BooleanField(default=True, verbose_name='Активный')
    is_staff = models.BooleanField(default=False, verbose_name='Администратор')
    is_superuser = models.BooleanField(default=False, verbose_name='Суперпользователь')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'phone', 'address']

    @property
    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        return f'https://ui-avatars.com/api/?size=150&background=random&name={self.slug}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('-date_joined',)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slugify(self, self.username)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reversed('account_detail', kvargs={'slug': self.slug})


@receiver(post_save, sender=User)
def create_user_custom(sender, instance, created, **kwargs):
    if created:
        Accounts.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_custom(sender, instance, **kwargs):
    instance.user.save()
