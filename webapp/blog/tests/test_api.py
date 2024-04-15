# test_api.py
from django.test import TestCase, Client, RequestFactory


# from rest_framework import status


class TestBlog(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_home_api(self):
        url = '/blog/'
        response = self.client.get(url)
        response.status_code = 200
