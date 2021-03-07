from django.urls import path
from accounts import views

app_name = "accounts"
urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("edit/", views.profile_edit, name="edit"),
    path("password_change/", views.password_change, name="password_change"),
    path("<username:username>/follow", views.follow, name="follow"),
    path("<username:username>/unfollow", views.unfollow, name="unfollow"),
]
