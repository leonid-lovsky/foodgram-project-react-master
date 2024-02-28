from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    # username_validator = ASCIIUsernameValidator()

    email = models.EmailField(
        _('email address'),
        unique=True,
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')
        ordering = ['email']

    def __str__(self):
        return f'{self.email}'
