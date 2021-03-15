# Generated by Django 3.1.7 on 2021-03-15 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='status',
            field=models.CharField(choices=[('verified', 'Верифицированный'), ('unverified', 'Неверифицированный')], default='unverified', max_length=10, verbose_name='Статус пользователя'),
        ),
    ]