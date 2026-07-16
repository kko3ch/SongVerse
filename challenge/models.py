import string

from django.db import models
from django.utils import timezone


class ChallengeDayManager(models.Manager):
    def get_or_create_today(self):
        today = timezone.localdate()
        challenge_day, _ = self.get_or_create(
            date=today,
            defaults={"letter": self._next_letter()},
        )
        return challenge_day

    def _next_letter(self):
        last = self.model.objects.order_by("-date").first()
        if last is None:
            return "A"
        alphabet = string.ascii_uppercase
        next_index = (alphabet.index(last.letter) + 1) % len(alphabet)
        return alphabet[next_index]


class ChallengeDay(models.Model):
    date = models.DateField(unique=True)
    letter = models.CharField(max_length=1)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = ChallengeDayManager()

    def __str__(self):
        return f"{self.date} — {self.letter}"