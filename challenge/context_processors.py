from datetime import datetime, time, timedelta

from django.utils import timezone

from .models import ChallengeDay


def todays_letter(request):
    challenge_day = ChallengeDay.objects.get_or_create_today()

    now = timezone.localtime()
    tomorrow_midnight = timezone.make_aware(
        datetime.combine(now.date() + timedelta(days=1), time.min)
    )
    seconds_left = int((tomorrow_midnight - now).total_seconds())

    return {
        "today_challenge": challenge_day,
        "today_letter": challenge_day.letter,
        "seconds_until_next_letter": max(seconds_left, 0),
    }