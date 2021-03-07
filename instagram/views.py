from instagram.models import Post
from instagram.forms import PostForm
from django.http import HttpRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()


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
    return render(
        request,
        "instagram/post_detail.html",
        {
            "post": post,
        },
    )


@login_required
def user_page(request, username):
    page_user = get_object_or_404(User, username=username, is_active=True)
    post_list = Post.objects.filter(author=page_user)
    # post_list_count = post_list.count()  # 실제 데이터베이스에 count 쿼리를 던지게 됩니다.

    # if request.user.is_authenticated:
    #     is_follow = request.user.following_set.filter(pk=page_user.pk).exists()
    # else:
    #     is_follow = False

    return render(
        request,
        "instagram/user_page.html",
        {
            "page_user": page_user,
            "post_list": post_list,
            # "post_list_count": post_list_count,
            # "is_follow": is_follow,
        },
    )
