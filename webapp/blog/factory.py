import factory
from blog.models import Post
from django.contrib.auth.models import User
from django.utils import timezone


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: f"User {n}")


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
