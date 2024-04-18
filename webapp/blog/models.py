from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class DefaultFieldModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Post(DefaultFieldModel):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)  # 문자, 숫자, 밑줄 또는 하이픈만 포함하는 짧은 레이블
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=2, choices=Status.choices, default=Status.DRAFT
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        # 역방향 관계를 지칭함 User 객체에서 post 속성을 이용할 수 있음
        # ex) user.blog_posts
        related_name="blog_posts",
    )

    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    def __str__(self):
        return self.title
