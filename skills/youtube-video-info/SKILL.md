---
name: youtube-video-info
description: Extract common YouTube video metadata (title, description, channel, duration, publish date, view/like counts, tags, and thumbnails) from a YouTube URL or video ID. Use when users ask for core video information without downloading media.
---

# Youtube Video Info

Use this skill for quick metadata extraction workflows, such as:
- "Get title, channel, and duration from this YouTube link."
- "Return the full description and publish date for this video."
- "Fetch video info as JSON to process in another script."

## Quick Start
```bash
python3 scripts/fetch_youtube_video_info.py "https://youtu.be/h_l8wCr7M2Q" --format markdown
```

## Commands
Markdown summary:
```bash
python3 scripts/fetch_youtube_video_info.py "<youtube-url>" --format markdown
```

Plain text output:
```bash
python3 scripts/fetch_youtube_video_info.py "<youtube-url>" --format plain
```

JSON output:
```bash
python3 scripts/fetch_youtube_video_info.py "<youtube-url>" --format json
```

Limit description length in text outputs:
```bash
python3 scripts/fetch_youtube_video_info.py "<youtube-url>" --format markdown --description-max-chars 400
```

## Supported Inputs
- Full YouTube URLs (`youtube.com/watch?v=...`, `youtube.com/shorts/...`, `youtube.com/embed/...`)
- Short URLs (`youtu.be/...`)
- Raw video IDs (11 chars)

## Output Fields
- `video_id`
- `title`
- `description`
- `channel` and `channel_id`
- `channel_url`
- `uploader` and `uploader_id`
- `published_at` (ISO-like: `YYYY-MM-DD`)
- `duration_seconds` and `duration_hms`
- `view_count`, `like_count`, `comment_count`
- `tags`, `categories`
- `thumbnail`
- `webpage_url`

## Requirements
- Python 3.9+
- `yt-dlp` CLI installed and available in `PATH` (`python3 -m pip install -U yt-dlp`)
- Network access to YouTube

## Decisions
- Uses `yt-dlp --dump-single-json --skip-download` for robust metadata extraction without downloading media.
- Keeps output formats deterministic (`plain`, `markdown`, `json`) to support both human and automation workflows.
