from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.SongVerseLoginView.as_view(), name="login"),
    path("logout/", views.SongVerseLogoutView.as_view(), name="logout"),
    path("u/<str:username>/", views.ProfileDetailView.as_view(), name="profile"),
]