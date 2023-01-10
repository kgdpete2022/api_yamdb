from django.contrib.auth.models import AbstractUser


from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class User(AbstractUser):
    ROLE_USER = 'user'
    ROLE_MODERATOR = 'moderator'
    ROLE_ADMIN = 'admin'

    ROLES = (
        (ROLE_USER, 'Пользователь'),
        (ROLE_MODERATOR, 'Модератор'),
        (ROLE_ADMIN, 'Администратор'),
    )

    username = models.CharField(
        max_length=150,
        verbose_name='Имя пользователя',
        unique=True,
        validators=[RegexValidator(
            regex=r'^[\w.@+-]+$')]
    )
    email = models.EmailField(
        max_length=254,
        verbose_name='email',
        unique=True
    )
    first_name = models.CharField(
        max_length=150,
        verbose_name='имя',
        blank=True
    )
    last_name = models.CharField(
        max_length=150,
        verbose_name='фамилия',
        blank=True
    )
    bio = models.TextField(
        verbose_name='биография',
        blank=True
    )
    role = models.CharField(
        max_length=max([len(role[0]) for role in ROLES]),
        verbose_name='роль',
        choices=ROLES,
        default=ROLE_USER
    )

    def __str__(self):
        return self.username

    @property
    def is_user(self):
        return self.role == self.ROLE_USER

    @property
    def is_moderator(self):
        return self.role == self.ROLE_MODERATOR

    @property
    def is_admin(self):
        return (
            self.role == self.ROLE_ADMIN
            or self.is_superuser
        )
