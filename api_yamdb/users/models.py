import random

from django.contrib.auth.models import AbstractUser
from django.core.mail import send_mail
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

    EMAIL_SUBJECT = 'Код подтверждения от сервиса YaMDB'
    EMAIL_MESSAGE = 'Ваш код подтверждения: {}'
    EMAIL_FROM = 'support@yamdb.ru'

    MIN_INTERVAL = 1e6
    MAX_INTERVAL = 1e7

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

    confirmation_code = models.IntegerField(
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

    def generate_confirmation_code(self):
        self.confirmation_code = random.randint(
            self.MIN_INTERVAL,
            self.MAX_INTERVAL
        )
        return self.confirmation_code

    def send_confirmation_code(self):
        send_mail(
            self.EMAIL_SUBJECT,
            self.EMAIL_MESSAGE.format(self.confirmation_code),
            self.EMAIL_FROM,
            [self.email]
        )
