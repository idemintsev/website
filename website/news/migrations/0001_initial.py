# Generated by Django 3.1.7 on 2021-03-04 07:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Теги')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'db_table': 'tags',
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(blank=True, max_length=40, verbose_name='Город')),
                ('phone_number', models.CharField(blank=True, max_length=20, verbose_name='Номер телефона')),
                ('written_news_quantity', models.IntegerField(default=0, verbose_name='Количество написанных новостей')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(db_index=True, max_length=120, verbose_name='Заголовок')),
                ('content', models.TextField(default='Нет текста', verbose_name='Текст новости')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('update_at', models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')),
                ('published', models.BooleanField(default=False, verbose_name='Опубликовать')),
                ('status', models.CharField(choices=[('h', 'Скрыть'), ('p', 'Показать')], default='p', max_length=1, verbose_name='Скрыть/показать на сайте')),
                ('tags', models.ManyToManyField(blank=True, help_text='тег', to='news.Tag', verbose_name='тег')),
            ],
            options={
                'verbose_name': 'Новости',
                'verbose_name_plural': 'Новости',
                'db_table': 'news',
                'ordering': ['-created_date'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Имя пользователя')),
                ('comment', models.TextField(verbose_name='Текст комментария')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('news', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='news.news')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'db_table': 'comments',
                'ordering': ['-created_date'],
            },
        ),
    ]
