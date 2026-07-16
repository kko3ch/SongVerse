# 🎵 SongVerse

**A daily music challenge, built with Django.** Every day reveals a new letter of the alphabet — submit your favorite song that starts with it, rate the day's picks, vote on the community's submissions, and climb the leaderboard. Along the way, SongVerse pulls in live trending music, new releases, and genre charts straight from YouTube.

---

## ✨ Features

- **Daily Alphabet Challenge** — a new letter (A → Z, then loops) is revealed automatically each day, with a live countdown to the next one.
- **Song Submissions** — type a song title, get live autocomplete suggestions (with thumbnails) powered by the YouTube Data API, and rate your pick with an animated half-star rating widget (1.0–5.0 in 0.5 steps).
- **Community Voting** — like submissions in real time via AJAX, no page reload.
- **Song-Based Leaderboard** — ranked by votes, with podium styling for the top 3, thumbnails, play links, and submitter credit. Filterable by Weekly / Monthly / All Time.
- **Live Music Discovery** — homepage sections for globally trending music, newest releases, genre-specific rows (Hip Hop, Afrobeats, Pop, Rock), and a dedicated Kenya trending + local-genre feed (Gengetone, Bongo Flava, Kenyan Afrobeats).
- **Accounts** — signup/login/logout with auto-created profiles, streak and stats tracking.
- **Custom auth-aware UI** — dark, glassmorphic design system with animated hero sections, a scrolling "now playing" ticker, and a surreal floating-G-clef submission page.

## 🛠 Tech Stack

- **Backend:** Django 5.x, SQLite (dev)
- **APIs:** YouTube Data API v3 (`google-api-python-client`)
- **Frontend:** Server-rendered Django templates, vanilla JS (no frontend framework), hand-rolled CSS design system
- **Config:** `python-decouple` for environment variables

## 📦 Project Structure

```
songverse/
├── core/            # Homepage
├── accounts/        # Signup, login, logout, profile
├── challenge/       # Daily letter engine (ChallengeDay model + business logic)
├── songs/           # Artists, songs, submissions, votes, YouTube integration
├── leaderboard/      # Vote-ranked leaderboard
├── templates/         # Project-level templates (base.html, partials/, per-app subfolders)
├── static/            # Favicon + any static assets
└── songverse/         # Project settings, root URLconf
```

## 🚀 Getting Started

### 1. Clone and set up a virtual environment

```bash
git clone https://github.com/kko3ch/songverse.git
cd songverse
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment variables

Create a `.env` file in the project root:

```
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
YOUTUBE_API_KEY=your-youtube-data-api-v3-key
```

You'll need a free [YouTube Data API v3](https://console.cloud.google.com/) key from Google Cloud Console (enable the API, create an API key, restrict it to YouTube Data API v3).

### 4. Run migrations and start the server

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Visit `http://127.0.0.1:8000`.

## 🔑 Environment Variables

| Variable | Description |
|---|---|
| `DJANGO_SECRET_KEY` | Django's cryptographic signing key — generate a unique one for production |
| `DJANGO_DEBUG` | `True` for local dev, `False` in production |
| `YOUTUBE_API_KEY` | YouTube Data API v3 key (10,000 free quota units/day) |

## 📊 API Quota Notes

Homepage YouTube data (trending, new releases, genre rows, Kenya feed) is cached for 2 hours per section to stay well within the free daily quota. Autocomplete search costs 100 quota units per debounced query.

## 🤝 Contributing

Issues and pull requests are welcome. This started as a portfolio/learning project, so if you spot something worth improving, feel free to open a PR.

## 📄 License

MIT — see [LICENSE](LICENSE).

## 🔗 Links

- GitHub: [github.com/kko3ch](https://github.com/kko3ch/)
- TikTok: [@nininitom](https://www.tiktok.com/@nininitom)