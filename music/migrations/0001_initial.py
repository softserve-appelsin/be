# Generated by Django 5.0.2 on 2024-03-21 19:18

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Album",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=50)),
                ("description", models.TextField(max_length=1000)),
                (
                    "image_album",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="image_for_album/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["jpg"]
                            )
                        ],
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="albums",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Track",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=100)),
                (
                    "file",
                    models.FileField(
                        upload_to="song/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["mp3"]
                            )
                        ],
                    ),
                ),
                ("create_at", models.DateTimeField(auto_now_add=True)),
                ("plays_count", models.PositiveIntegerField(default=0)),
                ("likes_count", models.PositiveIntegerField(default=0)),
                (
                    "image_track",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="image_for_track/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["jpg"]
                            )
                        ],
                    ),
                ),
                (
                    "album",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="music.album",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tracks",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "user_of_likes",
                    models.ManyToManyField(
                        blank=True,
                        related_name="likes_of_tracks",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="PlayList",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=50)),
                (
                    "image_playlist",
                    models.ImageField(
                        blank=True,
                        null=True,
                        upload_to="image_for_playlist/",
                        validators=[
                            django.core.validators.FileExtensionValidator(
                                allowed_extensions=["jpg"]
                            )
                        ],
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="play_lists",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "tracks",
                    models.ManyToManyField(
                        related_name="track_play_lists", to="music.track"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField(max_length=1000)),
                ("create_at", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="comments",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "track",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="track_comments",
                        to="music.track",
                    ),
                ),
            ],
        ),
    ]