from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.shortcuts import resolve_url


class User(AbstractUser):
    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMELE = "F", "Female"

    website_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(
        max_length=13,
        blank=True,
        validators=[RegexValidator(r"^010-?[1-9]\d{3}-?\d{4}$")],
    )
    gender = models.CharField(max_length=1, blank=True, choices=Gender.choices)
    avatar = models.ImageField(
        blank=True,
        upload_to="accounts/profile/%Y/%m/%d",
        help_text="48px * 48px png/jpg file!!",
    )
    follower_set = models.ManyToManyField(
        "self", blank=True, symmetrical=False, related_name="following_set"
    )

    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def avatar_url(self):
        if self.avatar:
            return self.avatar.url
        else:
            return resolve_url("pydenticon_image", self.username)
