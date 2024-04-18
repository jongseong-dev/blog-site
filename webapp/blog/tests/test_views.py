from blog.factory import PostFactory
from blog.models import Post
from django.test import Client
from django.test import TestCase
from rest_framework import status


class TestBlog(TestCase):
    def setUp(self):
        self.client = Client()
        self.test_case = PostFactory.create_batch(10)

    def test_post_list_200_OK(self):
        url = "/blog/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "blog/post/list.html")
        self.assertEqual(len(response.context["posts"]), 10)

    def test_post_detail_200_OK(self):
        url = f"/blog/{self.test_case[0].pk}/"
        response = self.client.get(url)
        self.assertTemplateUsed(response, "blog/post/detail.html")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_list_404_NOT_FOUND(self):
        Post.objects.all().delete()
        url = "/blog/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_detail_404_NOT_FOUND(self):
        url = "/blog/100039/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
