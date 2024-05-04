from django.test import TestCase

from blog.forms import EmailPostForm, CommentForm
from blog.forms import SearchForm


class EmailPostFormTests(TestCase):
    def test_valid_email_post_form(self):
        form = EmailPostForm(
            data={
                "name": "Test Name",
                "email": "test@example.com",
                "to": "to@example.com",
                "comments": "Test comment",
            }
        )
        self.assertTrue(form.is_valid())

    def test_invalid_email_post_form_no_email(self):
        form = EmailPostForm(
            data={
                "name": "Test Name",
                "email": "",
                "to": "to@example.com",
                "comments": "Test comment",
            }
        )
        self.assertFalse(form.is_valid())

    def test_invalid_email_post_form_no_to(self):
        form = EmailPostForm(
            data={
                "name": "Test Name",
                "email": "test@example.com",
                "to": "",
                "comments": "Test comment",
            }
        )
        self.assertFalse(form.is_valid())


class CommentFormTests(TestCase):
    def test_valid_comment_form(self):
        form = CommentForm(
            data={
                "name": "Test Name",
                "email": "test@example.com",
                "body": "Test comment body",
            }
        )
        self.assertTrue(form.is_valid())

    def test_invalid_comment_form_no_email(self):
        form = CommentForm(
            data={
                "name": "Test Name",
                "email": "",
                "body": "Test comment body",
            }
        )
        self.assertFalse(form.is_valid())

    def test_invalid_comment_form_no_body(self):
        form = CommentForm(
            data={"name": "Test Name", "email": "test@example.com", "body": ""}
        )
        self.assertFalse(form.is_valid())


class SearchFormTests(TestCase):
    def test_valid_search_form(self):
        form = SearchForm(data={"query": "post", "type": "nr"})
        self.assertTrue(form.is_valid())

    def test_invalid_search_form_no_query(self):
        form = SearchForm(data={"query": "", "type": "nr"})
        self.assertFalse(form.is_valid())

    def test_invalid_search_form_no_type(self):
        form = SearchForm(data={"query": "test", "type": ""})
        self.assertFalse(form.is_valid())

    def test_invalid_search_form_wrong_type(self):
        form = SearchForm(data={"query": "pp", "type": "wrong"})
        self.assertFalse(form.is_valid())
