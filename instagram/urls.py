from instagram.converters import UsernameConverter
from django.urls import path, register_converter
from instagram import views

register_converter(UsernameConverter, "username")

app_name = "instagram"
urlpatterns = [
    path("", views.index, name="index"),
    path("post/new/", views.post_new, name="post_new"),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path("<username:username>/", views.user_page, name="user_page"),
]
