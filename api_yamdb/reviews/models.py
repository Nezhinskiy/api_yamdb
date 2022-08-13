from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator
from django.db import models
from titles.models import Title

User = get_user_model()

DISPLAYED_LETTERS = 15

SCORE_CHOICES = (
    (1, 'Пришлось соврать, что смотрю порно, когда мама вошла в комнату'),
    (2, 'Каждый в моей комнате стал тупее'),
    (3, 'Лучше б я этого не видел'),
    (4, '3,6 - не отлично, но и не ужасно.'),
    (5, 'Видали мы и по-лучше'),
    (6, 'Потенциал не раскрыт'),
    (7, 'Пересматривать бы не стал'),
    (8, 'Моё уважение'),
    (9, 'Я ничего не понял, но сделаю вид, что всё понял'),
    (10, 'Рыдала вся маршрутка')
)


class Review(models.Model):
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Произведение',
        help_text='Произведение, к которой будет относиться ревью'
    )
    text = models.TextField(verbose_name='Текст отзыва')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='Автор отзыва'
    )
    score = models.PositiveIntegerField(
        validators=[MaxValueValidator(10)],
        choices=SCORE_CHOICES, verbose_name='Баллы'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'], name='unique_review')]
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:DISPLAYED_LETTERS]


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Отзыв',
        help_text='Отзыв, к которой будет относиться комментарий'
    )
    text = models.TextField(verbose_name='Текст комментария',
                            help_text='Текст нового комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор комментария'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text[:DISPLAYED_LETTERS]
