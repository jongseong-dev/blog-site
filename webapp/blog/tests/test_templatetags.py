from django.template import Template, Context
from django.test import TestCase
from django.utils.safestring import SafeString

from blog.factory import PostFactory, CommentFactory
from blog.templatetags.blog_tags import (
    get_most_commented_posts,
    total_posts,
    show_latest_posts,
    markdown_format,
)


class PostTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.posts = PostFactory.create_batch(10)
        for idx, post in enumerate(cls.posts):
            CommentFactory.create_batch(idx, post=post)

    def test_rendered_total_posts(self):
        result = Template("{% load blog_tags %}" "{% total_posts %}").render(
            Context()
        )
        self.assertEqual(result, "10")

    def test_get_total_posts(self):
        result = total_posts()
        self.assertEqual(result, 10)

    def test_rendered_show_latest_posts(self):
        result = Template(
            "{% load blog_tags %}" "{% show_latest_posts 3 %}"
        ).render(Context())
        self.assertEqual(result.count("Post"), 3)

    def test_get_show_latest_posts(self):
        result = show_latest_posts(3)
        self.assertEqual(result["latest_posts"].count(), 3)

    def test_get_most_commented_posts(self):
        result = get_most_commented_posts(5)
        self.assertEqual(result.count(), 5)

    def test_rendered_markdown_filter(self):
        markdown_text = (
            "# Heading\n\nThis is a paragraph "
            "with *italic* and **bold** text."
        )
        expected_html = (
            "<h1>Heading</h1>\n<p>This is a paragraph "
            "with <em>italic</em> "
            "and <strong>bold</strong> text.</p>"
        )

        template_str = "{% load blog_tags %}{{ markdown_text|markdown }}"
        template = Template(template_str)
        context = Context({"markdown_text": markdown_text})
        rendered_template = template.render(context)

        self.assertIsInstance(rendered_template, SafeString)
        self.assertEqual(rendered_template, expected_html)

    def test_get_markdown_filter(self):
        markdown_text = (
            "# Heading\n\nThis is a paragraph "
            "with *italic* and **bold** text."
        )
        expected_html = (
            "<h1>Heading</h1>\n<p>This is a paragraph "
            "with <em>italic</em> "
            "and <strong>bold</strong> text.</p>"
        )

        result = markdown_format(markdown_text)
        self.assertIsInstance(result, SafeString)
        self.assertEqual(result, expected_html)
