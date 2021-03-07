from django.urls import path
from instagram import views


app_name = "instagram"
urlpatterns = [
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path("post/new/", views.post_new, name="post_new"),
]
