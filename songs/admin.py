from django.contrib import admin
from .models import Artist, Genre, Song, Submission, Vote


admin.site.register(Genre)
admin.site.register(Artist)
admin.site.register(Song)
admin.site.register(Submission)
admin.site.register(Vote)