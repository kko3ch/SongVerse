from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from challenge.models import ChallengeDay
from .forms import SongSubmissionForm
from .models import Submission, Vote
from .youtube import search_songs


@login_required
def submit(request):
    if request.method == "POST":
        form = SongSubmissionForm(request.POST)
        if form.is_valid():
            challenge_day = ChallengeDay.objects.get_or_create_today()
            form.save(user=request.user, challenge_day=challenge_day)
            return redirect("challenge:today")
    else:
        form = SongSubmissionForm()
    return render(request, "songs/submit.html", {"form": form})


def autocomplete(request):
    query = request.GET.get("q", "")
    return JsonResponse({"results": search_songs(query)})


@login_required
def toggle_vote(request, submission_id):
    submission = get_object_or_404(Submission, pk=submission_id)
    vote, created = Vote.objects.get_or_create(submission=submission, user=request.user)
    if not created:
        vote.delete()
        liked = False
    else:
        liked = True
    return JsonResponse({"liked": liked, "vote_count": submission.votes.count()})