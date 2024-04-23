from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class DefaultFieldModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(status=Post.Status.PUBLISHED)


class Post(DefaultFieldModel):
    class Status(models.TextChoices):
        DRAFT = "DF", "Draft"
        PUBLISHED = "PB", "Published"

    title = models.CharField(max_length=250)
    slug = models.SlugField(
        max_length=250,
        unique_for_date="publish",  # 게시물의 게시 날짜를 기준으로 슬러그를 고유하게 정의하도록 함
    )  # 문자, 숫자, 밑줄 또는 하이픈만 포함하는 짧은 레이블
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

    objects = models.Manager()
    published = PublishedManager()

    class Meta:
        ordering = ["-publish"]
        indexes = [
            models.Index(fields=["-publish"]),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """
        객체의 표준 URL을 반환
        다른 layer 에서 해당 모델의 method를 통해 post_detail URL을 얻을 수 있음
        :return:
        """
        return reverse(
            "blog:post_detail",
            args=[
                self.publish.year,
                self.publish.month,
                self.publish.day,
                self.slug,
            ],
        )
