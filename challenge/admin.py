from django.contrib import admin
from .models import ChallengeDay


@admin.register(ChallengeDay)
class ChallengeDayAdmin(admin.ModelAdmin):
    list_display = ("date", "letter")