from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "author", "publish", "status")
    list_filter = (
        "status",
        "created_at",
        "author",
        "publish",
    )  # 해당 요소로 필터링 가능
    search_fields = ("title", "body")  # 해당 요소로 검색 타겟
    prepopulated_fields = {"slug": ("title",)}  # title 필드의 입력으로 slug 를 채우도록 함
    raw_id_fields = ("author",)  #
    date_hierarchy = "publish"  # 연월일 단계로 날짜를 고를 수 있는 네비게이션 링크
    ordering = ("status", "publish")
