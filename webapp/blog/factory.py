from random import randint

import factory
from django.contrib.auth.models import User
from django.utils import timezone
from django.utils.text import slugify
from faker import Faker
from taggit.models import Tag

from blog.models import Post

fake = Faker()


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"User {n}")


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag
        django_get_or_create = ("name",)

    name = factory.LazyAttribute(
        lambda obj: f"{fake.random_element(['sports', 'music', 'travel'])}"
    )
    slug = factory.LazyAttribute(lambda obj: slugify(obj.name))


class PostFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Post
        django_get_or_create = ("title",)

    title = factory.Sequence(lambda n: f"Post {n}")
    slug = factory.Sequence(lambda n: f"post-{n}")
    publish = factory.LazyFunction(timezone.now)
    author = factory.SubFactory(UserFactory)
    body = factory.Sequence(lambda n: f"Body {n}")
    status = factory.LazyAttribute(lambda o: Post.Status.PUBLISHED)

    @classmethod
    def _after_postgeneration(cls, instance, create, results=None):
        """
        Instance 생성 후 실행하는 함수

        :param instance:
        :param create:
        :param results:
        :return:
        """
        instance.tags.set(TagFactory.create_batch(randint(1, 3)))
