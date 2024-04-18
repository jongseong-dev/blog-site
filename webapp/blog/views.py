from blog.models import Post
from django.http import Http404
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render


def home(request):
    return JsonResponse({"page": "blog"})


def post_list(request):
    posts = Post.published.all()
    return render(request, "blog/post/list.html", {"posts": posts})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk, status=Post.Status.PUBLISHED)
    return render(request, "blog/post/detail.html", {"post": post})
