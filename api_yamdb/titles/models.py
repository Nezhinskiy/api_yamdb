import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


def max_value_current_year(value):
    return MaxValueValidator(
        datetime.date.today().year, "Год не может быть больше текущего")(
        value)


class Title(models.Model):
    """Название произведения."""
    name = models.TextField(
        'Название произведения',
        max_length='200',
        db_index=True,
        help_text='Введите название произведения'
    )
    year = models.PositiveIntegerField(
        'Год релиза',
        null=True,
        blank=True,
        db_index=True,
        help_text='Год релиза',
        validators=[MinValueValidator(1800), max_value_current_year]
    )
    description = models.TextField(
        'Описание',
        blank=True,
        help_text='Введите краткое описание произведения'
    )
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Категория',
        related_name='Category'
    )
    genre = models.ManyToManyField(
        'Genre',
        blank=True,
        verbose_name='Жанр',
        related_name='Genre'
    )
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ('year',)
        verbose_name='Произведение'
        verbose_name_plural='Произведения'


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
        ordering = ('name',)
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
        ordering = ('name',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'