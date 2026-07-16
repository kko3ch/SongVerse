from django.urls import path
from . import views

app_name = "challenge"

urlpatterns = [
    path("today/", views.today, name="today"),
]