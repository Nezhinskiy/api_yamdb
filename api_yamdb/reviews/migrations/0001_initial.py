# Generated by Django 2.2.16 on 2022-08-10 10:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('titles', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Текст нового ревью', verbose_name='Текст ревью')),
                ('score', models.IntegerField(choices=[(1, 'Пришлось соврать, что смотрю порно, когда мама вошла в комнату'), (2, 'Каждый в моей комнате стал тупее'), (3, 'Лучше б я этого не видел'), (4, '3,6 - не отлично, но и не ужасно.'), (5, 'Видали мы и по-лучше'), (6, 'Потенциал не раскрыт'), (7, 'Пересматривать бы не стал'), (8, 'Моё уважение'), (9, 'Я ничего не понял, но сделаю вид, что всё понял'), (10, 'Рыдала вся маршрутка')], verbose_name='Баллы')),
                ('pup_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('title', models.ForeignKey(help_text='Произведение, к которой будет относиться ревью', on_delete=django.db.models.deletion.CASCADE, related_name='reviews', to='titles.Title', verbose_name='Произведение')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(help_text='Текст нового комментария', verbose_name='Текст комментария')),
                ('pup_date', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('review', models.ForeignKey(help_text='Ревью, к которой будет относиться комментарий', on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='reviews.Review', verbose_name='Ревью')),
            ],
        ),
    ]
