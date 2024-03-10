from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import User


class Album(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='albums')
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000)
    image_album = models.ImageField(
        upload_to='image_for_album/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg'])])


class Track(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tracks')
    title = models.CharField(max_length=100)
    album = models.ForeignKey(Album, on_delete=models.SET_NULL, blank=True, null=True)
    file = models.FileField(
        upload_to='image_for_song/',
        validators=[FileExtensionValidator(allowed_extensions=['mp3'])]
    )
    create_at = models.DateTimeField(auto_now_add=True)
    plays_count = models.PositiveIntegerField(default=0)
    likes_count = models.PositiveIntegerField(default=0)
    user_of_likes = models.ManyToManyField(User, related_name='likes_of_tracks')

    def __str__(self):
        return f'{self.user} - {self.title}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    track = models.ForeignKey(Track, on_delete=models.CASCADE, related_name='track_comments')
    text = models.TextField(max_length=1000)
    create_at = models.DateTimeField(auto_now_add=True)


class PlayList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='play_lists')
    title = models.CharField(max_length=50)
    tracks = models.ManyToManyField(Track, related_name='track_play_lists')
    image_playlist = models.ImageField(
        upload_to='image_for_playlist/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg'])]
    )