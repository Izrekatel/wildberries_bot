from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """Модель пользователя."""
    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
    )
    first_name = models.CharField(
        _('first name'),
        max_length=150,
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
    )
    email = models.EmailField(
        _('email address'),
        max_length=254,
        unique=True
    )

    class Meta:
        ordering = ('username',)
        verbose_name = _('user')
        verbose_name_plural = _('users')
