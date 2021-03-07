from instagram.models import Comment, Post
from django import forms


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["photo", "caption", "location"]
        widgets = {
            "caption": forms.Textarea,
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["message"]
        widgets = {
            "message": forms.Textarea(attrs={"rows": 2}),
        }
