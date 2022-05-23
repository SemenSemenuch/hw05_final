from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django import forms
from django.core.cache import cache

from posts.models import Post, Group

User = get_user_model()


class PostTemplateTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            slug='test-slug',
            title='Заголовок'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Текст',
            group=cls.group,
        )

    def setUp(self):
        self.user = User.objects.create_user(username='IvanIvanuch')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    # Проверяем используемые шаблоны
    def test_pages_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_pages_names = {
            'posts/index.html': reverse('posts:index'),
            'posts/group_list.html': (
                reverse('posts:group_list', kwargs={'slug': 'test-slug'})),
            'posts/profile.html': (reverse(
                'posts:profile', kwargs={'username': 'IvanIvanuch'})),
            'posts/post_detail.html': (
                reverse('posts:post_detail', kwargs={'post_id': '1'}))
        }

        for template, reverse_name in templates_pages_names.items():
            with self.subTest(reverse_name=reverse_name):
                response = self.authorized_client.get(reverse_name)
                self.assertTemplateUsed(response, template)

    def test_post_edit_correst_template(self):
        response = self.authorized_client.get(reverse(
            'posts:post_edit', kwargs={'post_id': '1'}))
        self.assertTemplateUsed(response, 'posts/create_post.html')

    def test_create_post_correst_template(self):
        response = self.authorized_client.get(reverse('posts:post_create'))
        self.assertTemplateUsed(response, 'posts/create_post.html')


class PostTemplateTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='user_stas')
        cls.group = Group.objects.create(
            slug='test-slug',
            title='Заголовок'
        )
        Post.objects.create(
            author=cls.user,
            text='Текст',
            group=cls.group,
        )

    def setUp(self):
        cache.clear()
        self.post_id = 0
        self.user = User.objects.create_user(username='user_gena')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        response = self.authorized_client.get(reverse('posts:index'))
        form_fields = {
            'text': forms.fields.CharField,
            'author': forms.fields.ForeignKey(User),
            'group': forms.fields.ForeignKey(Group)
        }
        for value, expected in form_fields.items():
            with self.subTest(value=value):
                form_field = response.context.get('form').fields.get(value)
                self.assertIsInstance(form_field, expected)

    def test_group_list_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': 'test-slug'}))
        first_object = response.context['page_obj'][0]
        group_title_0 = first_object.group.title
        group_text_0 = first_object.text
        group_slug_0 = first_object.group.slug
        self.assertEqual(group_title_0, 'Заголовок')
        self.assertEqual(group_text_0, 'Текст')
        self.assertEqual(group_slug_0, 'test-slug')

    def test_post_detail_pages_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        response = (self.authorized_client.get(reverse(
            'posts:post_detail', kwargs={'post_id': '1'})))
        self.assertEqual(response.context.get('post').author, 'user_stas')
        self.assertEqual(response.context.get('post').text, 'Текст')
        self.assertEqual(
            response.context.get('post').post_id, self.post_id)

    def test_profile_show_correct_context(self):
        """Шаблон profile сформирован с правильным контекстом."""
        response = (self.authorized_client.get(reverse(
            'posts:profile', kwargs={'username': 'user_gena'})))
        self.assertEqual(response.context.get('post').author, 'user_gena')

    def test_post_edit_show_correct_context(self):
        """Шаблон post_edit сформирован с правильным контекстом."""
        response = (self.authorized_client.get(reverse(
            'posts:post_edit', kwargs={'post_id': '1'})))
        self.assertEqual(response.context.get('post').author, 'user_gena')
        self.assertEqual(response.context.get('post').text, 'Текст')
        self.assertEqual(response.context.get('post').post_id, self.post_id)

    def test_post_create_show_correct_context(self):
        """Шаблон post_create сформирован с правильным контекстом."""
        response = (self.authorized_client.get(reverse(
            'posts:post_create')))
        self.assertEqual(response.context.get('post').author, 'user_gena')
        self.assertEqual(response.context.get('post').text, 'Текст')
        self.assertEqual(response.context.get('post').post_id, self.post_id)


class PostTemplateTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            slug='test-slug',
            title='Заголовок'
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Текст',
            group=cls.group,
        )

    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(username='Stas')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)

    def test_post_create_show_correct_on_page(self):
        """Шаблон index отображает правильную группу."""
        response = self.authorized_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        group_slug = first_object.group.slug
        self.assertEqual(group_slug, 'test-slug')

    def test_group_list_show_correct_on_page(self):
        """Шаблон group_list отображает правильную группу."""
        response = self.client.get(reverse(
            'posts:group_list', kwargs={'slug': 'test-slug'}))
        first_object = response.context['page_obj'][0]
        group_slug = first_object.group.slug
        self.assertEqual(group_slug, 'test-slug')

    def test_profile_show_correct_on_page(self):
        """Шаблон profile отображает правильную группу."""
        response = (self.authorized_client.get(reverse(
            'posts:profile', kwargs={'username': 'auth'})))
        first_object = response.context['posts'][0]
        group_slug = first_object.group.title
        self.assertEqual(group_slug, 'Заголовок')
        self.assertIsNot(group_slug, 'Notest-slug')
