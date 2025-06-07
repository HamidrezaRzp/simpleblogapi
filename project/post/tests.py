from django.contrib.auth import get_user_model
from .models import Post
from django.test import TestCase
from django.urls import reverse, resolve
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from .serializers import PostSerializer
from .views import ListPosts, DetailPost

class PostTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            email='test@test.com',
            username='test',
            name='test',
            password='password'
        )
        cls.post = Post.objects.create(
            title='Title',
            body='this is body',
            author=cls.user
        )

    def test_model_post(self):
        self.assertEqual(self.post.author.username, 'test')
        self.assertEqual(self.post.title, 'Title')
        self.assertEqual(self.post.body, 'this is body')
        self.assertEqual(str(self.post), 'Title')
        self.assertIsNotNone(self.post.created_at)
        self.assertIsNotNone(self.post.updated_at)

class PostSerializerTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='ser@test.com',
            username='ser',
            name='ser',
            password='password'
        )
        self.post = Post.objects.create(
            title='SerTitle',
            body='Ser body',
            author=self.user
        )

    def test_post_serialization(self):
        serializer = PostSerializer(self.post)
        data = serializer.data
        self.assertEqual(data['title'], 'SerTitle')
        self.assertEqual(data['body'], 'Ser body')
        self.assertEqual(data['author'], self.user.id)
        self.assertIn('created_at', data)

class PostURLTests(TestCase):
    def test_postslist_url_resolves(self):
        url = reverse('postslist')
        self.assertEqual(resolve(url).func.view_class, ListPosts)

    def test_postdetail_url_resolves(self):
        url = reverse('postdetail', args=[1])
        self.assertEqual(resolve(url).func.view_class, DetailPost)

class PostAPITests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='api@test.com',
            username='api',
            name='api',
            password='password'
        )
        self.client = APIClient()
        self.post = Post.objects.create(
            title='API Title',
            body='API body',
            author=self.user
        )
        self.list_url = reverse('postslist')
        self.detail_url = reverse('postdetail', args=[self.post.id])

    def test_list_posts(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_post_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'New Post',
            'body': 'New body',
            'author': self.user.id
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

    def test_create_post_unauthenticated(self):
        data = {
            'title': 'No Auth',
            'body': 'No Auth body',
            'author': self.user.id
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

    def test_retrieve_post(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'API Title')

    def test_update_post_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'title': 'Updated Title',
            'body': 'Updated body',
            'author': self.user.id
        }
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Title')

    def test_update_post_unauthenticated(self):
        data = {
            'title': 'Should Update',
            'body': 'Should Update',
            'author': self.user.id
        }
        response = self.client.put(self.detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Should Update')

    def test_delete_post_authenticated(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())

    def test_delete_post_unauthenticated(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Post.objects.filter(id=self.post.id).exists())


