# 🎵 SongVerse

**A daily music challenge, built with Django.** Every day reveals a new letter of the alphabet — submit your favorite song that starts with it, rate the day's picks, vote on the community's submissions, and climb the leaderboard. Along the way, SongVerse pulls in live trending music, new releases, and genre charts straight from YouTube.

**🔴 Live:** [songverse.onrender.com](https://songverse.onrender.com)

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

- **Backend:** Django 5.x
- **Database:** PostgreSQL in production ([Neon](https://neon.tech)), SQLite for local dev
- **APIs:** YouTube Data API v3 (`google-api-python-client`)
- **Frontend:** Server-rendered Django templates, vanilla JS (no frontend framework), hand-rolled CSS design system
- **Config:** `python-decouple` for environment variables
- **Hosting:** [Render](https://render.com) (web service) + [Neon](https://neon.tech) (database)
- **Production serving:** Gunicorn (WSGI server) + WhiteNoise (static files)

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
├── build.sh            # Render build script (install, collectstatic, migrate, superuser)
└── songverse/         # Project settings, root URLconf
```

## 🚀 Getting Started (local development)

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
| `DATABASE_URL` | Postgres connection string (production only — falls back to local SQLite if unset) |
| `DJANGO_SUPERUSER_USERNAME` | Production only — auto-creates an admin user on deploy |
| `DJANGO_SUPERUSER_EMAIL` | Production only — paired with the above |
| `DJANGO_SUPERUSER_PASSWORD` | Production only — paired with the above |

## 📊 API Quota Notes

Homepage YouTube data (trending, new releases, genre rows, Kenya feed) is cached for 2 hours per section to stay well within the free daily quota. Autocomplete search costs 100 quota units per debounced query.

## ☁️ Deployment (Render + Neon)

SongVerse runs on a completely free, indefinite hosting stack — no credit card, no forced expiry, no trial period ending. It's split across two services on purpose:

- **[Render](https://render.com)** hosts the actual running Django app (the web service). Its free web-service tier doesn't expire — it just spins down after ~15 minutes of inactivity and takes 30–50 seconds to wake back up on the next request. That cold start is the only real trade-off of the free tier.
- **[Neon](https://neon.tech)** hosts the PostgreSQL database. This is the key piece: **Render's own free Postgres offering auto-deletes itself 90 days after creation** — fine for a demo, not for something meant to stay live. Neon's free tier has no such expiry; it "scales to zero" (pauses compute when idle, wakes on the next query) instead of being deleted on a timer, and requires no credit card. Pointing Render's `DATABASE_URL` at a Neon database instead of Render's own Postgres is what makes this whole stack sustainable long-term at $0.

### How it's wired together

1. **GitHub → Render**: pushing to `main` auto-triggers a Render deploy.
2. **`build.sh`** runs on every deploy:
   ```bash
   pip install -r requirements.txt
   python manage.py collectstatic --no-input
   python manage.py migrate
   python manage.py createsuperuser --noinput || true
   ```
   The `createsuperuser --noinput` step reads the `DJANGO_SUPERUSER_*` environment variables to create an admin account automatically — necessary because Render's free tier has no shell/SSH access, so there's no interactive terminal to run `createsuperuser` normally. The `|| true` lets the build succeed on every subsequent deploy even though that user already exists.
3. **`DATABASE_URL`** (set in Render's environment variables) points at Neon rather than a Render-managed database, via `dj_database_url.config()` in `settings.py`.
4. **WhiteNoise** serves static files (CSS, favicon) directly from the Django process — no separate static host or CDN needed for a project this size.

### Deploying your own copy

1. Push your fork to GitHub.
2. Create a free [Neon](https://neon.tech) project, copy its connection string.
3. Create a free [Render](https://render.com) Web Service pointing at your repo:
   - Build Command: `bash build.sh`
   - Start Command: `gunicorn songverse.wsgi:application`
4. Add all the environment variables listed in the table above (use the Neon connection string for `DATABASE_URL`).
5. Deploy — Render builds, runs migrations against Neon, and creates your admin user automatically.

## 🤝 Contributing

Issues and pull requests are welcome. This started as a portfolio/learning project, so if you spot something worth improving, feel free to open a PR.

## 📄 License

MIT — see [LICENSE](LICENSE).

## 🔗 Links

- Live site: [songverse.onrender.com](https://songverse.onrender.com)
- GitHub: [github.com/kko3ch](https://github.com/kko3ch/)
- TikTok: [@nininitom](https://www.tiktok.com/@nininitom)