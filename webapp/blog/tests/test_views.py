from random import randint

from django.test import Client
from django.test import TestCase
from django.urls import reverse
from rest_framework import status

from blog.factory import PostFactory
from blog.factory import TagFactory
from blog.forms import SEARCH_TYPE_CHOICES
from blog.models import Comment
from blog.models import Post


class PostListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.tags = [TagFactory() for _ in range(randint(1, 3))]
        cls.post_list = PostFactory.create_batch(10)
        cls.url = reverse("blog:post_list")
        cls.url_with_tag = reverse(
            "blog:post_list_by_tag", args=[cls.tags[-1]]
        )

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_get_post_list_200_OK(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTemplateUsed(response, "blog/post/list.html")
        self.assertEqual(len(response.context["posts"]), 3)

    def test_get_post_list_404_NOT_FOUND(self):
        response = self.client.get(self.url, {"page": 1000})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_post_list_filter_by_tag(self):
        response_with_tag = self.client.get(self.url_with_tag)
        self.assertEqual(response_with_tag.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Post.published.filter(tags__in=[self.tags[-1]]).count(),
            response_with_tag.context["posts"].paginator.count,
        )


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

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

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

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_get_post_share_200_OK(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
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


class PostCommentViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.post = PostFactory.create()
        self.url = reverse("blog:post_comment", args=[self.post.id])

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()

    def test_post_comment_200_OK(self):
        response = self.client.post(
            self.url,
            {
                "name": "Test User",
                "email": "testuser@example.com",
                "body": "This is a test comment.",
            },
        )
        self.assertTemplateUsed(response, "blog/post/comment.html")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.count(), 1)

    def test_post_comment_NOT_VALID_INPUT(self):
        response = self.client.post(
            self.url, {"name": "", "email": "not an email", "body": ""}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Comment.objects.count(), 0)

    def test_post_comment_404_NOT_FOUND(self):
        url = reverse("blog:post_comment", args=[1000])
        response = self.client.post(
            url,
            {
                "name": "Test User",
                "email": "testuser@example.com",
                "body": "This is a test comment.",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class PostSearchViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.posts = PostFactory.create_batch(10, title="test")
        cls.url = reverse("blog:post_search")

    def test_get_post_search_type_normal_200_OK(self):
        response = self.client.get(
            self.url, {"query": "test", "type": SEARCH_TYPE_CHOICES[0][0]}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Body", str(response.content))

    def test_get_post_search_wrong_type_200_OK(self):
        response = self.client.get(
            self.url, {"query": "test", "type": "wrong"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("Select a valid choice.", str(response.content))

    def test_get_post_search_empty_query_200_OK(self):
        response = self.client.get(
            self.url, {"query": "", "type": SEARCH_TYPE_CHOICES[0][0]}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("This field is required", str(response.content))
