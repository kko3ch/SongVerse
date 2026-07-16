from django.conf import settings
from googleapiclient.discovery import build

MUSIC_CATEGORY_ID = "10"  # YouTube's fixed category ID for Music


def _client():
    return build("youtube", "v3", developerKey=settings.YOUTUBE_API_KEY)


def _format_count(n):
    """1234567 -> '1.2M', 45000 -> '45K' — for compact stat display."""
    n = int(n)
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)


def _enrich_with_stats(video_ids):
    """One videos.list call (statistics part) for a whole batch of IDs —
    fetches view/like counts for up to 50 videos in a single request
    instead of one call per video."""
    if not video_ids:
        return {}
    youtube = _client()
    response = youtube.videos().list(
        part="statistics,contentDetails",
        id=",".join(video_ids),
    ).execute()
    stats = {}
    for item in response.get("items", []):
        s = item.get("statistics", {})
        stats[item["id"]] = {
            "views": _format_count(s.get("viewCount", 0)),
            "likes": _format_count(s.get("likeCount", 0)) if "likeCount" in s else None,
            "duration": item.get("contentDetails", {}).get("duration", ""),
        }
    return stats


def get_trending_music(max_results=10, region_code="US"):
    """Most popular music videos right now (chart endpoint), enriched with
    view counts. region_code lets us pull Kenya's chart (KE) separately
    from the global/US one."""
    youtube = _client()
    response = youtube.videos().list(
        part="snippet,statistics",
        chart="mostPopular",
        videoCategoryId=MUSIC_CATEGORY_ID,
        maxResults=max_results,
        regionCode=region_code,
    ).execute()

    results = []
    for item in response.get("items", []):
        snippet = item["snippet"]
        stats = item.get("statistics", {})
        results.append({
            "video_id": item["id"],
            "title": snippet["title"],
            "channel": snippet["channelTitle"],
            "thumbnail": snippet["thumbnails"]["medium"]["url"],
            "url": f"https://www.youtube.com/watch?v={item['id']}",
            "views": _format_count(stats.get("viewCount", 0)),
        })
    return results


def get_new_releases(max_results=10):
    """Newest music uploads, sorted by publish date rather than popularity —
    the "just dropped" feed. Uses search.list with order=date."""
    youtube = _client()
    response = youtube.search().list(
        part="snippet",
        q="official music video",
        type="video",
        videoCategoryId=MUSIC_CATEGORY_ID,
        order="date",
        maxResults=max_results,
    ).execute()

    items = response.get("items", [])
    video_ids = [i["id"]["videoId"] for i in items]
    stats = _enrich_with_stats(video_ids)

    results = []
    for item in items:
        vid = item["id"]["videoId"]
        snippet = item["snippet"]
        results.append({
            "video_id": vid,
            "title": snippet["title"],
            "channel": snippet["channelTitle"],
            "thumbnail": snippet["thumbnails"]["medium"]["url"],
            "url": f"https://www.youtube.com/watch?v={vid}",
            "published_at": snippet["publishedAt"],
            "views": stats.get(vid, {}).get("views"),
        })
    return results


def get_music_by_genre(genre_query, max_results=8):
    """Powers per-genre rows on the homepage (Hip Hop, Afrobeats,
    Gengetone, etc). A targeted search.list scoped to the Music category."""
    youtube = _client()
    response = youtube.search().list(
        part="snippet",
        q=genre_query,
        type="video",
        videoCategoryId=MUSIC_CATEGORY_ID,
        order="viewCount",
        maxResults=max_results,
    ).execute()

    results = []
    for item in response.get("items", []):
        vid = item["id"]["videoId"]
        snippet = item["snippet"]
        results.append({
            "video_id": vid,
            "title": snippet["title"],
            "channel": snippet["channelTitle"],
            "thumbnail": snippet["thumbnails"]["medium"]["url"],
            "url": f"https://www.youtube.com/watch?v={vid}",
        })
    return results


def search_songs(query, max_results=6):
    """Powers the autocomplete field on the submission form."""
    if not query or len(query) < 2:
        return []

    youtube = _client()
    response = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        videoCategoryId=MUSIC_CATEGORY_ID,
        maxResults=max_results,
    ).execute()

    results = []
    for item in response.get("items", []):
        snippet = item["snippet"]
        results.append({
            "video_id": item["id"]["videoId"],
            "title": snippet["title"],
            "channel": snippet["channelTitle"],
            "thumbnail": snippet["thumbnails"]["default"]["url"],
            "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
        })
    return results