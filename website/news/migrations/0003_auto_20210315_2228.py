from django.contrib.auth.models import Permission
from django.db import migrations


def create_groups(apps, schema_editor):
    """
    Создает две группы пользователей: Модератор и Верифицированный пользователь.
    Верифицированный пользователь может добавлять и просматривать новости.
    Модератор может добавлять, просматривать, редактировать, удалять новости, присваивать другим пользователям статус
    "верифицированный пользователь".
    """
    Group = apps.get_model('auth', 'Group')
    if not Group.objects.exists():
        view_permission = Permission.objects.get(name='Can view news')
        add_permission = Permission.objects.get(name='Can add news')
        change_permission = Permission.objects.get(name='Can change news')
        delete_permission = Permission.objects.get(name='Can delete news')
        view_profile_permission = Permission.objects.get(name='Can view profile')
        change_profile_permission = Permission.objects.get(name='Can change profile')
        view_user_permission = Permission.objects.get(name='Can view user')
        change_user_permission = Permission.objects.get(name='Can change user')
        moderator = Group(name='Модератор')
        verified_user = Group(name='Верифицированный пользователь')
        moderator.save()
        verified_user.save()
        moderator.permissions.add(
            view_permission.id, add_permission.id, change_permission.id, delete_permission.id,
            view_profile_permission.id, change_profile_permission.id, view_user_permission.id, change_user_permission.id
        )
        verified_user.permissions.add(view_permission.id, add_permission.id)
        moderator.save()
        verified_user.save()


class Migration(migrations.Migration):
    atomic = False

    dependencies = [
        ('news', '0002_profile_status'),
    ]

    operations = [
        migrations.RunPython(create_groups),
    ]
