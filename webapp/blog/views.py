from blog.forms import CommentForm
from blog.forms import EmailPostForm
from blog.models import Post
from django.conf import settings
from django.core.mail import send_mail
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.core.paginator import Paginator
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.views.generic import ListView
from taggit.models import Tag


def post_list(request, tag_slug=None):
    posts = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])
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
        request,
        "blog/post/list.html",
        {"posts": posts_with_pagination, "tag": tag},
    )


class PostListView(ListView):
    """
    Alternative post list view
    """

    queryset = Post.published.all()
    # 컨텍스트 변수로 "posts"를 지정한다. 지정하지 않을 경우 기본 변수는 "object_list"이다.
    context_object_name = "posts"
    paginate_by = 3
    template_name = "blog/post/list.html"


def post_detail(request, year: int, month: int, day: int, post: Post):
    post = get_object_or_404(
        Post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=post,
        status=Post.Status.PUBLISHED,
    )
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(
        request,
        "blog/post/detail.html",
        {"post": post, "comments": comments, "form": form},
    )


def post_share(request, post_id: int):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    sent = False
    if request.method == "POST":
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read {post.title}"
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            send_mail(subject, message, settings.EMAIL_HOST_USER, [cd["to"]])
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request,
        "blog/post/share.html",
        {"post": post, "form": form, "sent": sent},
    )


@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, status=Post.Status.PUBLISHED)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # 데이터베이스에 저장하지 않고 Comment 객체 만들기
        comment = form.save(commit=False)
        # 댓글에 게시물 할당하기
        comment.post = post
        # 댓글을 데이터베이스에 저장
        comment.save()
    return render(
        request,
        "blog/post/comment.html",
        {"post": post, "form": form, "comment": comment},
    )
