from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile"
    )
    bio = models.CharField(max_length=280, blank=True)

    songs_submitted = models.PositiveIntegerField(default=0)
    total_likes_received = models.PositiveIntegerField(default=0)
    current_streak = models.PositiveIntegerField(default=0)
    last_submission_date = models.DateField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username