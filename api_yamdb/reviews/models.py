from django.contrib.auth import get_user_model
from django.db import models

from titles.models import Title

User = get_user_model()

SCORES = (
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
        help_text='Произведение, к которой будет относиться ревью',
    )
    text = models.TextField(verbose_name='Текст ревью',
                            help_text='Текст нового ревью')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Автор',
    )
    score = models.IntegerField(choices=SCORES, verbose_name='Баллы')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True,
    )


class Comment(models.Model):
    review = models.ForeignKey(
        Review,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Ревью',
        help_text='Ревью, к которой будет относиться комментарий',
    )
    text = models.TextField(verbose_name='Текст комментария',
                            help_text='Текст нового комментария')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Автор',
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации',
        db_index=True,
    )
