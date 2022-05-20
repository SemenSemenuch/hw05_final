import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.test import Client, TestCase, override_settings
from django.conf import settings
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache


from posts.models import Post, Group
from posts.forms import PostForm


User = get_user_model()

TEMP_MEDIA_ROOT = tempfile.mkdtemp(dir=settings.BASE_DIR)


@override_settings(MEDIA_ROOT=TEMP_MEDIA_ROOT)
class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = PostForm()

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEMP_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        cache.clear()
        self.user = User.objects.create_user(username='test')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.group = Group.objects.create(
            title='Заголовок',
            slug='test-slug',)
        self.test_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        post_count = Post.objects.count()
        self.small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x02\x00'
            b'\x01\x00\x80\x00\x00\x00\x00\x00'
            b'\xFF\xFF\xFF\x21\xF9\x04\x00\x00'
            b'\x00\x00\x00\x2C\x00\x00\x00\x00'
            b'\x02\x00\x01\x00\x00\x02\x02\x0C'
            b'\x0A\x00\x3B'
        )
        self.uploaded = SimpleUploadedFile(
            name='small.gif',
            content=self.small_gif,
            content_type='image/gif'
        )
        form_data = {
            'title': 'Тестовый заголовок',
            'text': 'Тестовый текст',
            'image': self.uploaded,
        }
        self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), post_count + 1)

    def test_post_index_page_show_correct_context(self):
        """Шаблон index сформирован с правильным контекстом."""
        uploaded = SimpleUploadedFile(
            name='test1.gif ',
            content=self.test_gif,
            content_type='image/gif'
        )
        self.post_test = Post.objects.create(
            text='Test',
            author=self.user,
            group=self.group,
            image=uploaded
        )
        response = self.authorized_client.get(reverse('posts:index'))
        first_object = response.context['page_obj'][0]
        post_author_0 = first_object.author.username
        post_text_0 = first_object.text
        post_group_0 = first_object.group.title
        post_image_0 = first_object.image
        self.assertEqual(post_author_0, 'test')
        self.assertEqual(post_text_0, 'Test')
        self.assertEqual(post_group_0, f'{self.group}')
        self.assertEqual(post_image_0, 'posts/test1.gif')

    def test_post_profile_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        uploaded = SimpleUploadedFile(
            name='test2.gif',
            content=self.test_gif,
            content_type='image/gif'
        )

        self.post_test = Post.objects.create(
            text='Test',
            author=self.user,
            group=self.group,
            image=uploaded
        )
        response = self.authorized_client.get(
            reverse('posts:profile',
                    kwargs={'username': f'{self.user.username}'}))
        first_object = response.context['page_obj'][0]
        post_author_0 = first_object.author.username
        post_text_0 = first_object.text
        post_group_0 = first_object.group.title
        post_image_0 = first_object.image
        self.assertEqual(post_author_0, 'test')
        self.assertEqual(post_text_0, 'Test')
        self.assertEqual(post_group_0, f'{self.group}')
        self.assertEqual(post_image_0, 'posts/test2.gif')

    def test_post_group_page_show_correct_context(self):
        """Шаблон group_list сформирован с правильным контекстом."""
        uploaded = SimpleUploadedFile(
            name='test3.gif',
            content=self.test_gif,
            content_type='image/gif'
        )
        self.post_test = Post.objects.create(
            text='Test',
            author=self.user,
            group=self.group,
            image=uploaded
        )
        response = self.authorized_client.get(
            reverse('posts:group_list', kwargs={'slug': 'test-slug'})
        )
        first_object = response.context['page_obj'][0]
        post_author_0 = first_object.author.username
        post_text_0 = first_object.text
        post_group_0 = first_object.group.title
        post_image_0 = first_object.image
        self.assertEqual(post_author_0, 'test')
        self.assertEqual(post_text_0, 'Test')
        self.assertEqual(post_group_0, f'{self.group}')
        self.assertEqual(post_image_0, 'posts/test3.gif')

    def test_post_detail_pages_show_correct_context(self):
        """Шаблон post_detail сформирован с правильным контекстом."""
        uploaded = SimpleUploadedFile(
            name='test4.gif',
            content=self.test_gif,
            content_type='image/gif'
        )
        self.post_test = Post.objects.create(
            text='Test',
            author=self.user,
            group=self.group,
            image=uploaded
        )
        response = (self.authorized_client.get(
            reverse('posts:post_detail',
                    kwargs={'post_id': f'{self.post_test.id}'})))
        self.assertEqual(response.context.get('post').image, 'posts/test4.gif')

    def test_no_image_to_load(self):
        """Форма создает запись в Post но не изображение."""
        post_count = Post.objects.count()
        test_image = 'просто текст, не картинка'
        form_data = {
            'text': 'текст',
            'group': self.group,
            'image': test_image,
        }
        response_image = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        self.assertEqual(Post.objects.count(), post_count)
        self.assertFormError(
            response_image,
            'form',
            'image',
            'Ошибка при выборе типа поля'
        )
