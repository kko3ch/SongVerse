from datetime import timedelta

from django.db.models import Count, Q
from django.shortcuts import render
from django.utils import timezone

from songs.models import Submission

PERIODS = {"weekly": 7, "monthly": 30, "all": None}


def leaderboard(request):
    period = request.GET.get("period", "weekly")
    days = PERIODS.get(period, 7)

    vote_filter = Q(votes__isnull=False)
    if days is not None:
        since = timezone.now() - timedelta(days=days)
        vote_filter &= Q(votes__created_at__gte=since)

    ranked_submissions = (
        Submission.objects.select_related("song", "song__artist", "user")
        .annotate(vote_total=Count("votes", filter=vote_filter))
        .filter(vote_total__gt=0)
        .order_by("-vote_total")[:50]
    )

    return render(request, "leaderboard/leaderboard.html", {
        "ranked_submissions": ranked_submissions,
        "active_period": period,
    })