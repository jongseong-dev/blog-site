# test_api.py
from django.test import Client
from django.test import RequestFactory
from django.test import TestCase


class TestWebApp(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()

    def test_healthcheck(self):
        url = "/health/"
        response = self.client.get(url)
        response.status_code = 200
