from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    USER_STATUS = [
        ('verified', 'Верифицированный'),
        ('unverified', 'Неверифицированный')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    city = models.CharField(max_length=40, blank=True, verbose_name='Город')
    phone_number = models.CharField(max_length=20, blank=True, verbose_name='Номер телефона')
    written_news_quantity = models.IntegerField(default=0, verbose_name='Количество написанных новостей')
    status = models.CharField(max_length=10, choices=USER_STATUS, default='unverified', verbose_name='Статус пользователя')


class News(models.Model):
    STATUS_CHOICES = [
        ('h', 'Скрыть'),
        ('p', 'Показать')
    ]
    title = models.CharField(max_length=120, db_index=True, verbose_name='Заголовок')
    content = models.TextField(default='Нет текста', verbose_name='Текст новости')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    update_at = models.DateTimeField(auto_now=True, verbose_name='Дата редактирования')
    published = models.BooleanField(default=False, verbose_name='Опубликовать')
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='p',
                              verbose_name='Скрыть/показать на сайте')
    tags = models.ManyToManyField('Tag', blank=True, verbose_name='тег', help_text='тег')

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'news'
        ordering = ['-created_date']
        verbose_name = 'Новости'
        verbose_name_plural = 'Новости'

    def get_absolute_url(self):
        return reverse('news_details', kwargs={'pk': self.id})


class Tag(models.Model):
    name = models.CharField(max_length=150, verbose_name='Теги')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tags'
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Comment(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя пользователя')
    comment = models.TextField(verbose_name='Текст комментария')
    created_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    news = models.ForeignKey(News, default=None, on_delete=models.CASCADE, related_name='comments')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'comments'
        ordering = ['-created_date']
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
