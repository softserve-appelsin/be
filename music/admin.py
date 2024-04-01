from django.contrib import admin
from .models import Track, Album, PlayList, Comment

admin.site.register(Track)
admin.site.register(Album)
admin.site.register(PlayList)
admin.site.register(Comment)

