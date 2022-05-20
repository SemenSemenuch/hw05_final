from django.db import models
from django.contrib.auth import get_user_model

from core.models import CreatedModel

User = get_user_model()


class Group(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название сообщества'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name="URL"
    )
    description = models.TextField(
        verbose_name='Описание сообщества'
    )

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    text = models.TextField(
        max_length=200,
        verbose_name='Содержимое поста',
        help_text='Введите текст поста'
    )
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='Автор поста'
    )
    group = models.ForeignKey(
        Group,
        max_length=200,
        blank=True, null=True,
        on_delete=models.SET_NULL,
        related_name='groups',
        verbose_name='Название сообщества',
        help_text='Группа, к которой относиться пост'
    )
    image = models.ImageField(
        'Картинка',
        upload_to='posts/',
        blank=True, null=True,
        help_text='Загрузите картинку'
    )

    def __str__(self) -> str:
        return self.text[:15]

    class Meta:
        ordering = ['pub_date']


class Comment(CreatedModel):
    post = models.ForeignKey(
        Post,
        blank=True, null=True,
        on_delete=models.CASCADE,
        related_name='comments',
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="comments"
    )
    text = models.TextField(
        max_length=200,
        verbose_name='Содержимое поста',
        help_text='Введите текст поста'
    )

    def __str__(self) -> str:
        return self.user.username


class Follow(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='follower'
                             )
    author = models.ForeignKey(User,
                               on_delete=models.CASCADE,
                               related_name='following'
                               )

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'
        constraints = [models.UniqueConstraint(fields=['user', 'author'],
                                               name='unique_follow')]

    def __str__(self):
        return f'Подписка на {self.author}'
