from blog.models import Post
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render


def post_list(request):
    posts = Post.published.all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get("page", 1)
    try:
        posts_with_pagination = paginator.page(page_number)
    except PageNotAnInteger:
        # 페이지 번호가 정수가 아닌 경우 결과의 첫 페이지를 전달
        posts_with_pagination = paginator.page(1)
    except EmptyPage:
        # 페이지 번호가 범위를 벗어난 경우 결과의 마지막 페이지를 전달
        posts_with_pagination = paginator.page(paginator.num_pages)
    return render(
        request, "blog/post/list.html", {"posts": posts_with_pagination}
    )


def post_detail(request, year: int, month: int, day: int, post: Post):
    post = get_object_or_404(
        Post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=post,
        status=Post.Status.PUBLISHED,
    )
    return render(request, "blog/post/detail.html", {"post": post})
