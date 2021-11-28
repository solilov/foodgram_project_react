# from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        blank=False,
        null=False,
        verbose_name=_('email address')
    )
    first_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name=_('first name')
    )
    last_name = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name=_('last name'),
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        ordering = ['username']

    def __str__(self):
        return self.get_full_name()
