from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView

from .forms import SignUpForm
from .models import Profile


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = "accounts/signup.html"
    success_url = reverse_lazy("core:home")

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)
        return response


class SongVerseLoginView(LoginView):
    template_name = "accounts/login.html"


class SongVerseLogoutView(LogoutView):
    next_page = reverse_lazy("core:home")


class ProfileDetailView(DetailView):
    model = Profile
    template_name = "accounts/profile.html"
    context_object_name = "profile"

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user__username=self.kwargs["username"])