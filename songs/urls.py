from django.urls import path
from . import views

app_name = "songs"

urlpatterns = [
    path("submit/", views.submit, name="submit"),
    path("autocomplete/", views.autocomplete, name="autocomplete"),
    path("vote/<int:submission_id>/", views.toggle_vote, name="toggle_vote"),
]
