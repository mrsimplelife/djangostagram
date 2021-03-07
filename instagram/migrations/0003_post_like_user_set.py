# Generated by Django 3.1.7 on 2021-03-07 07:46

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('instagram', '0002_auto_20210307_0719'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='like_user_set',
            field=models.ManyToManyField(blank=True, related_name='like_post_set', to=settings.AUTH_USER_MODEL),
        ),
    ]
