from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from http import HTTPStatus
from django.core.cache import cache

from posts.models import Post, Group
from posts.forms import PostForm


User = get_user_model()


class PostFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.guest_client = Client
        cls.author = User.objects.create_user(username='auth')
        cls.author_client = Client()
        cls.author_client.force_login(cls.author)
        cls.group = Group.objects.create(
            slug='test-slug',
            title='Заголовок'
        )
        cls.post = Post.objects.create(
            author=cls.author,
            text='Текст',
            group=cls.group
        )
        cls.form = PostForm()

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        post_count = Post.objects.count()
        form_data = {
            'author': PostFormTests.author,
            'text': 'Текст',
            'group': PostFormTests.post.group.id
        }
        response = PostFormTests.author_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': 'auth'}))
        self.assertEqual(Post.objects.count(), post_count + 1)
        post = Post.objects.first()
        self.assertEqual(post.text, form_data['text'])
        self.assertEqual(post.group.id, form_data['group'])
        self.assertEqual(post.author, self.author)

    def setUp(self):
        cache.clear()
        self.user_Goga = User.objects.create_user(username='userGoga')
        self.user_Gosha = User.objects.create_user(username='userGosha')
        self.authorized_client_1 = Client()
        self.authorized_client_2 = Client()
        self.authorized_client_1.force_login(self.user_Goga)
        self.authorized_client_2.force_login(self.user_Gosha)
        self.post_test = Post.objects.create(
            text='Test',
            author=self.user_Goga
        )

    def test_no_loginning_user(self):
        """Неавторизованный пользователь не может создать Post."""
        response = self.client.post('/create', kwargs={'text': 'test'})
        self.assertEqual(response.status_code, HTTPStatus.MOVED_PERMANENTLY)

    def test_post_edit_of_loginning_user(self):
        """Авторизованный пользователь не может редактироать чужой Post."""
        response = self.authorized_client_2.post('/edit', kwargs={
            'post_id': f'{self.post_test.id}', 'text': 'test'})
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_post_edit(self):
        """Валидная форма изменяет запись Post в базе данных."""
        form_data = {
            'group': self.group.id,
            'text': 'Тестовый текст'
        }
        PostFormTests.author_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True,
        )
        post_2 = Post.objects.get(id=self.group.id)
        self.client.get(f'/TestUser/{post_2.id}/edit/')
        form_data = {
            'text': 'Отредактированный текст',
            'group': self.group.id
        }
        response_edit = PostFormTests.author_client.post(
            reverse('posts:post_edit',
                    kwargs={
                        'post_id': post_2.id
                    }),
            data=form_data,
            follow=True,
        )
        post_2 = Post.objects.get(id=self.group.id)
        self.assertEqual(response_edit.status_code, HTTPStatus.OK)
        self.assertEqual(post_2.text, form_data['text'])
