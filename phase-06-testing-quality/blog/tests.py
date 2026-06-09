from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Post, Profile


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass123")
        self.post = Post.objects.create(
            title="Test Post",
            content="Test content",
            author=self.user,
            published=True,
        )

    def test_post_str(self):
        self.assertEqual(str(self.post), "Test Post")

    def test_published_manager_filters_correctly(self):
        Post.objects.create(
            title="Draft Post",
            content="Not published",
            author=self.user,
            published=False,
        )
        self.assertEqual(Post.published_posts.all().count(), 1)
        self.assertEqual(Post.published_posts.all().first().title, "Test Post")

    def test_default_manager_returns_all(self):
        Post.objects.create(
            title="Draft Post",
            content="Not published",
            author=self.user,
            published=False,
        )
        self.assertEqual(Post.objects.all().count(), 2)


class ProfileSignalTest(TestCase):
    def test_profile_auto_created_on_user_creation(self):
        user = User.objects.create_user(username="newuser", password="pass123")
        self.assertTrue(Profile.objects.filter(user=user).exists())

    def test_profile_not_duplicated_on_user_update(self):
        user = User.objects.create_user(username="updateuser", password="pass123")
        user.first_name = "Updated"
        user.save()
        self.assertEqual(Profile.objects.filter(user=user).count(), 1)


class PostAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="pass123")
        self.token = Token.objects.create(user=self.user)
        self.client = APIClient()
        self.post = Post.objects.create(
            title="API Test Post",
            content="Content here",
            author=self.user,
            published=True,
        )

    def test_list_posts_unauthenticated(self):
        response = self.client.get("/api/posts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_post_without_token_returns_401(self):
        response = self.client.post(
            "/api/posts/",
            {"title": "New", "content": "Test", "published": True},
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_post_with_token_returns_201(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.post(
            "/api/posts/",
            {"title": "New Post", "content": "Some content", "published": True},
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

    def test_author_set_from_token_not_request_body(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.post(
            "/api/posts/",
            {
                "title": "Authored Post",
                "content": "Testing author injection",
                "published": True,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        created_post = Post.objects.get(title="Authored Post")
        self.assertEqual(created_post.author, self.user)

    def test_filter_by_published(self):
        Post.objects.create(
            title="Draft",
            content="...",
            author=self.user,
            published=False,
        )
        response = self.client.get("/api/posts/?published=true")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for post in response.data["results"]:
            self.assertTrue(post["published"])

    def test_search_by_title(self):
        response = self.client.get("/api/posts/?search=API+Test")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"][0]["title"], "API Test Post")

    def test_retrieve_single_post(self):
        response = self.client.get(f"/api/posts/{self.post.pk}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "API Test Post")
