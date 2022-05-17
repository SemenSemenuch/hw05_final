from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from http import HTTPStatus

from posts.models import Post, Comment

User = get_user_model()


class PostCommentTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')

    def setUp(self):
        self.user = User.objects.create_user(username='IvanIvanuch')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.post = Post.objects.create(
            author=self.user,
            text='Текст',
        )
        self.comment = Comment.objects.create(
            author=self.user,
            text='Text',
            post=self.post
        )

    def test_post_edit_correst_template(self):
        """Доступность комментариев для неавторизированных пользователей."""
        response = self.client.get(
            reverse('posts:add_comment', kwargs={'post_id': self.post.pk}))
        self.assertEqual(response.status_code, HTTPStatus.FOUND.value)
        response_1 = self.authorized_client.get(
            reverse('posts:add_comment', kwargs={'post_id': self.post.pk}))
        self.assertEqual(response_1.status_code, HTTPStatus.FOUND.value)

    def test_create_post_correst_template(self):
        """Появление комментария на странице поста."""
        form_data = {
            'text': 'Текст',
            'post': self.post
        }
        self.authorized_client.post(reverse(
            'posts:add_comment', kwargs={'post_id': self.post.pk}),
            data=form_data,
            follow=True
        )
        self.assertTrue(
            Comment.objects.filter(
                text='Текст').exists
        )
