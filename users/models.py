from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    PROFILE_TYPES = (
        ('Artist', 'Artist'),
        ('Listener', 'Listener')
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_type = models.CharField(max_length=100, choices=PROFILE_TYPES)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    bio = models.TextField(blank=True)
