from blog.factory import PostFactory
from blog.forms import EmailPostForm
from blog.models import Post
from blog.views import post_share
from django.http import Http404
from django.test import Client
from django.test import RequestFactory
from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class PostListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.post_list = PostFactory.create_batch(10)
        self.url = reverse("blog:post_list")

    def test_post_list_200_OK(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "blog/post/list.html")
        self.assertEqual(len(response.context["posts"]), 3)

    def test_post_list_404_NOT_FOUND(self):
        response = self.client.get(self.url, {"page": 1000})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PostDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.post = PostFactory.create()
        self.url = reverse(
            "blog:post_detail",
            args=[
                self.post.publish.year,
                self.post.publish.month,
                self.post.publish.day,
                self.post.slug,
            ],
        )

    def test_post_detail_404_NOT_FOUND(self):
        Post.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_detail_200_OK(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, "blog/post/detail.html")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PostShareViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.post = PostFactory.create()
        self.url = reverse("blog:post_share", args=[self.post.id])

    def test_get_post_share_200_OK(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post/share.html")

    def test_post_post_share_200_OK(self):
        response = self.client.post(
            self.url,
            {
                "name": "Test User",
                "email": "testuser@example.com",
                "to": "recipient@example.com",
                "comments": "Check out this post!",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.context["sent"])

    def test_get_post_share_404_NOT_FOUND(self):
        Post.objects.all().delete()
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
