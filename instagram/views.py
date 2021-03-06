from instagram.models import Post
from instagram.forms import PostForm
from django.http import HttpRequest
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required


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
            return redirect("/")
    else:
        form = PostForm()
    return render(
        request,
        "instagram/post_form.html",
        {
            "form": form,
        },
    )
