from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    ROLE_CHOICES = (
        (ADMIN, 'Администратор'),
        (MODERATOR, 'Модератор'),
        (USER, 'Пользователь'),
    )

    email = models.EmailField(
        verbose_name='Email',
        unique=True,
    )

    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
    )

    role = models.CharField(
        verbose_name='Роль',
        max_length=15,
        choices=ROLE_CHOICES,
        default=USER,
    )

    confirmation_code = models.UUIDField(
        verbose_name='Код подтверждения',
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN
