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

    email = models.EmailField(
        verbose_name='Email',
        unique=True,
        help_text='Введите адрес email',
    )

    bio = models.TextField(
        verbose_name='Биография',
        blank=True,
        help_text='Введите текст биографии',
    )

    role = models.CharField(
        verbose_name='Роль',
        max_length=15,
        choices=ROLE_CHOICES,
        default=USER,
        help_text='Выберите роль пользователя',
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
        return (self.role == self.ADMIN) or self.is_superuser

    def send_confirmation_code(self, token):
        send_mail(
            self.EMAIL_SUBJECT,
            self.EMAIL_MESSAGE.format(token),
            self.EMAIL_FROM,
            [self.email]
        )
