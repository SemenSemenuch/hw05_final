from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from http import HTTPStatus

from posts.models import Post, Group


User = get_user_model()


class FollowTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Group.objects.create(
            title='Тестовое сообщество',
            slug='test-slug',
            description='Тестовое описание'
        )

    def setUp(self):
        self.user2 = User.objects.create_user(username='test2')
        self.user = User.objects.create_user(username='test')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.post_test = Post.objects.create(
            text='Test',
            author=self.user2
        )

    def test_follow(self):
        response = (self.authorized_client.get(
            reverse('posts:profile_follow',
                    kwargs={'username': f'{self.user2.username}'})))
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_unfollow(self):
        self.authorized_client.get(
            reverse('posts:profile_follow',
                    kwargs={'username': f'{self.user2.username}'}))
        response_2 = (self.authorized_client.get(
            reverse('posts:profile_unfollow',
                    kwargs={'username': f'{self.user2.username}'})))
        self.assertEqual(response_2.status_code, HTTPStatus.FOUND)

    def test_follow_index(self):
        self.authorized_client.get(
            reverse('posts:profile_follow',
                    kwargs={'username': f'{self.user2.username}'}))
        response = self.authorized_client.get(
            reverse(
                'posts:follow_index'
            )
        )
        first_object = response.context['page_obj'][0]
        post_author_0 = first_object.author.username
        post_text_0 = first_object.text
        self.assertEqual(post_author_0, 'test2')
        self.assertEqual(post_text_0, 'Test')
        
    def test_follow_following_client(self):
        self.authorized_client.force_login(self.user2)
        response = self.authorized_client.get(
            reverse(
                'posts:follow_index'
            )
        )
        long_page = len(response.context['page_obj'])
        self.assertEqual(long_page, 0)