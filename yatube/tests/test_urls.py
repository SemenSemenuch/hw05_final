from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from http import HTTPStatus


from posts.models import Group, Post


User = get_user_model()


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='test-slug'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            group=cls.group,
            text='Тестовый текст',
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_urls_uses_correct_template(self):
        """URL-адрес доступные любому пользователю."""
        url_names = {
            'index': '/',
            'group/<slug>/': '/group/test-slug/',
            'profile/<str:username>': f'/profile/{self.user}/',
            'posts/<post_id>': '/posts/1/',
            'posts/<post_id>/edit': '/posts/1/edit/',
            'create/': '/create/',
        }

        for template, address in url_names.items():
            with self.subTest(address=address):
                response = self.authorized_client.get(address)
                self.assertEqual(response.status_code, HTTPStatus.OK.value)

    def test_url_not_found(self):
        response = self.authorized_client.get('/unexisting_page/')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND.value)
