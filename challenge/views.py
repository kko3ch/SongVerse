from django.db.models import Count
from django.shortcuts import render

from .models import ChallengeDay
from songs.models import Submission


def today(request):
    challenge_day = ChallengeDay.objects.get_or_create_today()
    submissions = (
        Submission.objects.filter(challenge_day=challenge_day)
        .select_related("song", "song__artist", "user")
        .annotate(vote_total=Count("votes"))
        .order_by("-vote_total")
    )
    return render(request, "challenge/today.html", {
        "challenge_day": challenge_day,
        "submissions": submissions,
    })