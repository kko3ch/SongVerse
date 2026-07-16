from decimal import Decimal

from django import forms

from songs.models import Artist, Song, Submission
from songs.youtube import search_songs
import html


class SongSubmissionForm(forms.Form):
    """Two visible fields (song, comment) plus the star rating widget.
    Artist, thumbnail, and the YouTube link are all resolved automatically:

    1. If the user picks a suggestion from the autocomplete dropdown, JS
       fills all three hidden fields from that suggestion.
    2. If they typed a song and submitted without picking a suggestion,
       `save()` below falls back to one live YouTube search and uses the
       first result for whichever hidden fields are still empty.
    """

    your_song = forms.CharField(max_length=255, label="Your Song")
    artist_name = forms.CharField(max_length=200, required=False, widget=forms.HiddenInput())
    thumbnail_url = forms.URLField(required=False, widget=forms.HiddenInput())
    youtube_url = forms.URLField(required=False, widget=forms.HiddenInput())
    rating = forms.DecimalField(
        min_value=Decimal("1.0"),
        max_value=Decimal("5.0"),
        decimal_places=1,
        widget=forms.HiddenInput(),
        label="Your Rating",
    )
    comment = forms.CharField(
        max_length=280,
        required=False,
        widget=forms.Textarea(attrs={"rows": 2}),
        label="Comment (optional)",
    )

    def clean_rating(self):
        rating = self.cleaned_data["rating"]
        doubled = rating * 2
        if doubled != int(doubled):
            raise forms.ValidationError("Rating must be in half-star increments.")
        return rating

    def _fallback_result(self):
        """One shared lookup, cached on the instance, so we don't fire the
        YouTube search three times (once per missing field)."""
        if not hasattr(self, "_fallback_cache"):
            results = search_songs(self.cleaned_data["your_song"])
            self._fallback_cache = results[0] if results else None
        return self._fallback_cache

    def _resolve_artist_name(self):
        given = self.cleaned_data.get("artist_name", "").strip()
        if given:
            return given
        fallback = self._fallback_result()
        return fallback["channel"] if fallback else "Unknown Artist"

    def _resolve_thumbnail_url(self):
        given = self.cleaned_data.get("thumbnail_url", "").strip()
        if given:
            return given
        fallback = self._fallback_result()
        return fallback["thumbnail"] if fallback else ""

    def _resolve_youtube_url(self):
        given = self.cleaned_data.get("youtube_url", "").strip()
        if given:
            return given
        fallback = self._fallback_result()
        return fallback["url"] if fallback else ""

    def save(self, user, challenge_day):
        artist, _ = Artist.objects.get_or_create(name=self._resolve_artist_name())
        song = Song.objects.create(
            title=html.unescape(self.cleaned_data["your_song"]),
            artist=artist,
            thumbnail_url=self._resolve_thumbnail_url(),
            youtube_url=self._resolve_youtube_url(),
        )
        return Submission.objects.create(
            song=song,
            user=user,
            challenge_day=challenge_day,
            rating=self.cleaned_data["rating"],
            comment=self.cleaned_data.get("comment", ""),
        )