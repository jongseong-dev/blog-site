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
        self.assertEqual(len(response.context["posts"]), 3)

    def test_post_detail_200_OK(self):
        post = self.test_case[0]
        url = (
            f"/blog/{post.publish.year}/{post.publish.month}/"
            f"{post.publish.day}/{post.slug}/"
        )
        response = self.client.get(url)
        self.assertTemplateUsed(response, "blog/post/detail.html")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_list_404_NOT_FOUND(self):
        Post.objects.all().delete()
        url = "/blog/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_post_detail_404_NOT_FOUND(self):
        post = self.test_case[0]
        url = (
            f"/blog/{post.publish.year + 1000}/"
            f"{post.publish.month}/{post.publish.day}/"
            f"{post.slug}/"
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
