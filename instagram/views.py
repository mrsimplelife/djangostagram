from datetime import timedelta
from sys import prefix
from django.db.models.query_utils import Q
from instagram.models import Post
from instagram.forms import CommentForm, PostForm
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()


@login_required
def comment_new(request: HttpRequest, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == "POST":
        form = CommentForm(request.POST, request.FILES)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                return render(
                    request,
                    "instagram/_comment.html",
                    {
                        "comment": comment,
                    },
                )
            return redirect(comment.post)
    else:
        form = CommentForm()
    return render(
        request,
        "instagram/comment_form.html",
        {
            "form": form,
        },
    )


@login_required
def post_new(request: HttpRequest):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post: Post = form.save(commit=False)
            post.author = request.user
            post.save()
            post.extract_tag_list()
            messages.success(request, "post saved!!")
            return redirect(post)
    else:
        form = PostForm()
    return render(
        request,
        "instagram/post_form.html",
        {
            "form": form,
        },
    )


@login_required
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comment_form = CommentForm()
    return render(
        request,
        "instagram/post_detail.html",
        {"post": post, "comment_form": comment_form},
    )


@login_required
def post_unlike(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.remove(request.user)
    messages.success(request, f"unliked #{post.pk}")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)


@login_required
def post_like(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.like_user_set.add(request.user)
    messages.success(request, f"liked #{post.pk}")
    redirect_url = request.META.get("HTTP_REFERER", "root")
    return redirect(redirect_url)


@login_required
def user_page(request, username):
    page_user = get_object_or_404(User, username=username, is_active=True)
    post_list = Post.objects.filter(author=page_user)
    post_list_count = post_list.count()
    is_follow = request.user.following_set.filter(pk=page_user.pk).exists()
    isMine = request.user == page_user
    return render(
        request,
        "instagram/user_page.html",
        {
            "page_user": page_user,
            "post_list": post_list,
            "post_list_count": post_list_count,
            "is_follow": is_follow,
            "isMine": isMine,
        },
    )


@login_required
def index(request):
    suggested_user_list = (
        get_user_model()
        .objects.all()
        .exclude(pk=request.user.pk)
        .exclude(pk__in=request.user.following_set.all())[:3]
    )
    timesince = timezone.now() - timedelta(days=3)
    post_list = (
        Post.objects.all()
        .filter(Q(author=request.user) | Q(author__in=request.user.following_set.all()))
        .filter(created_at__gte=timesince)
    )
    comment_form = CommentForm(auto_id=False)
    return render(
        request,
        "instagram/index.html",
        {
            "comment_form": comment_form,
            "suggested_user_list": suggested_user_list,
            "post_list": post_list,
        },
    )
