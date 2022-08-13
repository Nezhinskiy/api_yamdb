from django.db import models

from .validators import max_value_current_year


class Category(models.Model):
    """Тип произведения."""
    name = models.TextField(
        'Категория произведения',
        max_length=60,
        unique=True,
        db_index=True,
        help_text='Введите категорию произведения'
    )
    slug = models.SlugField(
        verbose_name='Категория произведения',
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Genre(models.Model):
    """Название жанра."""
    name = models.TextField(
        'Название жанра',
        max_length=60,
        unique=True,
        db_index=True,
        help_text='Введите название жанра'
    )
    slug = models.SlugField(
        verbose_name='Жанр',
        unique=True
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Title(models.Model):
    """Название произведения."""
    name = models.TextField(
        'Название произведения',
        max_length=200,
        db_index=True,
        help_text='Введите название произведения'
    )
    year = models.PositiveIntegerField(
        'Год релиза',
        null=True,
        blank=True,
        db_index=True,
        help_text='Год релиза',
        validators=[max_value_current_year]
    )
    description = models.TextField(
        'Описание',
        null=True,
        blank=True,
        help_text='Введите краткое описание произведения'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория',
        related_name='titles'
    )
    genre = models.ManyToManyField(
        Genre,
        null=True,
        blank=True,
        verbose_name='Жанр',
        related_name='titles'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('year',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
