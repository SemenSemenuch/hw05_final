from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from posts.models import Post, Group

User = get_user_model()


class PaginatorViewsTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

    def setUp(self):
        self.count = 20
        self.group = Group.objects.create(
            title='Тестовое сообщество',
            slug='testslug',
            description='Тестовое описание'
        )
        self.user = User.objects.create_user(username='test')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        for i in range(self.count):
            self.post_test = Post.objects.create(
                text='Test',
                author=self.user,
                group=self.group
            )

    def test_index_posts_pagination(self):
        """Проверка количества записей Post в шаблоне index."""
        response_first = self.authorized_client.get(reverse('posts:index'))
        paginator = response_first.context['page_obj'].paginator
        count_pages = paginator.num_pages + 1
        count_posts = 0
        for i in range(1, count_pages):
            response = self.authorized_client.get(
                reverse('posts:index') + f'?page={i}')
            count_posts += len(response.context['page_obj'])
        self.assertEqual(count_posts, self.count)

    def test_group_list_pagination(self):
        """Проверка количества записей Post в шаблоне group_list."""
        response_first = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': 'testslug'}))
        paginator = response_first.context['page_obj'].paginator
        count_pages = paginator.num_pages
        count_posts = 0
        for i in range(count_pages):
            response = self.authorized_client.get(reverse(
                'posts:group_list', kwargs={'slug': 'testslug'})
                + f'?page={i}')
            count_posts += len(response.context['page_obj'])
        self.assertEqual(count_posts, self.count)

    def test_profile_pagination(self):
        """Проверка количества записей Post в шаблоне profile."""
        response_first = self.authorized_client.get(
            reverse('posts:profile', kwargs={'username': self.user}))
        paginator = response_first.context['page_obj'].paginator
        count_pages = paginator.num_pages
        count_posts = 0
        for i in range(count_pages):
            response = self.authorized_client.get(reverse(
                'posts:profile', kwargs={'username': self.user})
                + f'?page={i}')
            count_posts += len(response.context['page_obj'])
        self.assertEqual(count_posts, self.count)
