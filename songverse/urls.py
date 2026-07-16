from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("challenge/", include("challenge.urls")),
    path("songs/", include("songs.urls")),
    path("leaderboard/", include("leaderboard.urls")),
    path("accounts/", include("accounts.urls")),
]