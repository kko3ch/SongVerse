from django.core.cache import cache
from django.db.models import Count
from django.shortcuts import render

from challenge.models import ChallengeDay
from songs.models import Submission
from songs.youtube import get_music_by_genre, get_new_releases, get_trending_music

CACHE_TTL = 60 * 60 * 2  # 2 hours — keeps us well under the 10k/day quota

GENRE_ROWS = [
    ("Hip Hop", "hip hop official music video"),
    ("Afrobeats", "afrobeats official music video"),
    ("Pop", "pop official music video"),
    ("Rock", "rock official music video"),
]

KENYA_GENRE_ROWS = [
    ("Gengetone", "gengetone official music video"),
    ("Bongo Flava", "bongo flava official music video"),
    ("Kenyan Afrobeats", "kenyan afrobeats official music video"),
]


def _cached(key, fetch_fn):
    value = cache.get(key)
    if value is None:
        try:
            value = fetch_fn()
        except Exception:
            value = []
        cache.set(key, value, CACHE_TTL)
    return value


def home(request):
    challenge_day = ChallengeDay.objects.get_or_create_today()

    trending = _cached("yt_trending", get_trending_music)
    new_releases = _cached("yt_new_releases", get_new_releases)
    kenya_trending = _cached("yt_trending_ke", lambda: get_trending_music(region_code="KE"))

    genre_rows = []
    for label, query in GENRE_ROWS:
        videos = _cached(f"yt_genre_{label.replace(' ', '_')}", lambda q=query: get_music_by_genre(q))
        if videos:
            genre_rows.append({"label": label, "videos": videos})

    kenya_genre_rows = []
    for label, query in KENYA_GENRE_ROWS:
        videos = _cached(f"yt_genre_ke_{label.replace(' ', '_')}", lambda q=query: get_music_by_genre(q))
        if videos:
            kenya_genre_rows.append({"label": label, "videos": videos})

    top_selected = (
        Submission.objects.filter(challenge_day=challenge_day)
        .values("song__title", "song__artist__name")
        .annotate(pick_count=Count("id"))
        .order_by("-pick_count")[:5]
    )

    top_voted = (
        Submission.objects.filter(challenge_day=challenge_day)
        .select_related("song", "song__artist")
        .annotate(vote_total=Count("votes"))
        .order_by("-vote_total")[:5]
    )

    return render(request, "core/home.html", {
        "trending_youtube": trending,
        "new_releases": new_releases,
        "genre_rows": genre_rows,
        "kenya_trending": kenya_trending,
        "kenya_genre_rows": kenya_genre_rows,
        "top_selected": top_selected,
        "top_voted": top_voted,
    })