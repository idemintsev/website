from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from news.models import News, Comment, Profile, Tag


class CommentInLine(admin.TabularInline):
    model = Comment


class TagsInLine(admin.TabularInline):
    model = Tag


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    actions = ['mark_as_hidden', 'mark_as_published']

    def mark_as_hidden(self, request, queryset):
        queryset.update(status='h')

    def mark_as_published(self, request, queryset):
        queryset.update(status='p')

    mark_as_hidden.short_description = 'Скрыть на сайте'
    mark_as_published.short_description = 'Показывать на сайте'

    list_display = ['id', 'title', 'created_date', 'update_at', 'published', 'status']
    list_filter = ['created_date', 'update_at', 'status']
    search_fields = ['title', 'content']
    inlines = [CommentInLine]
    fieldsets = (
        ('Заголовок и текст новости', {'fields': ('title', 'content', 'tags')}),
        ('Опубликовать текст новости', {'fields': ('published',)})
    )


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    actions = ['deleted_by_administrator']

    list_display = ['id', 'name']
    list_filter = ['name']
    search_fields = ['name']

    short_description = 'Теги'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    actions = ['deleted_by_administrator']

    list_display = ['id', 'name', 'created_date', 'news', 'short_comment']
    list_filter = ['created_date', 'name']
    search_fields = ['name', 'comment']

    def short_comment(self, obj):
        return obj.comment if len(obj.comment) < 16 else (obj.comment[:15] + '...')

    short_comment.short_description = 'Комментарий'

    def deleted_by_administrator(self, request, queryset):
        queryset.update(comment='Удалено администратором')

    deleted_by_administrator.short_description = 'Удалить текст комментария'


class UserInLine(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Дополнительные данные'


class WebUserAdmin(UserAdmin):
    actions = ['mark_as_verified', 'mark_as_unverified']

    def mark_as_verified(self, request, queryset):
        for obj in queryset:
            obj.profile.status = 'verified'
            obj.profile.save()

    def mark_as_unverified(self, request, queryset):
        for obj in queryset:
            obj.profile.status = 'unverified'
            obj.profile.save()

    mark_as_verified.short_description = 'Верифицированный пользователь'
    mark_as_unverified.short_description = 'Неверифицированный пользователь'

    inlines = (UserInLine,)
    list_display = ['id', 'username', 'first_name', 'last_name', 'news_creation', 'user_status']
    search_fields = ['username', 'first_name', 'last_name']

    def news_creation(self, obj):
        return obj.has_perm('website.add_news')

    def user_status(self, obj):
        return obj.profile.status

    news_creation.short_description = 'Создание новостей'
    user_status.short_description = 'Статус пользователя'


admin.site.unregister(User)
admin.site.register(User, WebUserAdmin)
