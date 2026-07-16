from django.conf import settings
from django.db import models
from django.utils.text import slugify


class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Artist(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Song(models.Model):
    title = models.CharField(max_length=255)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name="songs")
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True, blank=True)
    thumbnail_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} — {self.artist}"

class Submission(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name="submissions")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="submissions")
    challenge_day = models.ForeignKey("challenge.ChallengeDay", on_delete=models.CASCADE, related_name="submissions")
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=5.0)
    comment = models.CharField(max_length=280, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user", "challenge_day"], name="one_submission_per_user_per_day")
        ]

    def __str__(self):
        return f"{self.user} → {self.song}"

class Vote(models.Model):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="votes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["submission", "user"], name="one_vote_per_user_per_submission")
        ]