from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


class User(AbstractUser):

    class Gender(models.TextChoices):
        MALE = 'M', "Male"
        FEMELE = 'F', "Female"

    website_url = models.URLField(blank=True)
    bio = models.TextField(blank=True)
    phone_number = models.CharField(max_length=13, blank=True,
                                    validators=[RegexValidator(r'^010-?[1-9]\d{3}-?\d{4}$')])
    gender = models.CharField(max_length=1, blank=True,
                              choices=Gender.choices)
    avatar = models.ImageField(blank=True,
                               upload_to='accounts/profile/%Y/%m/%d', help_text='48px * 48px png/jpg file!!')
