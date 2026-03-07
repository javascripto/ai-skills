---
name: youtube-thumbnail-links
description: Generate YouTube thumbnail URLs in standard sizes (`default`, `mqdefault`, `hqdefault`, `sddefault`, `maxresdefault`) from a YouTube URL or video ID. Use when a user asks for thumbnail links, clickable Markdown links, multi-size thumbnail output, or rendered Markdown image preview for YouTube videos.
---

# Youtube Thumbnail Links

Use the helper script to normalize YouTube links, extract `videoId`, and generate thumbnail URLs in plain text or Markdown.

## Quick Start
```bash
python3 scripts/generate_youtube_thumbnails.py "https://youtu.be/h_l8wCr7M2Q" --format markdown
```

## Commands
Generate clickable Markdown links:
```bash
python3 scripts/generate_youtube_thumbnails.py "<youtube-url>" --format markdown
```

Generate clickable Markdown links and append the best image rendered:
```bash
python3 scripts/generate_youtube_thumbnails.py "<youtube-url>" --format markdown --with-max-image
```

Generate plain URL list:
```bash
python3 scripts/generate_youtube_thumbnails.py "<youtube-url>" --format plain
```

Generate JSON:
```bash
python3 scripts/generate_youtube_thumbnails.py "<youtube-url>" --format json
```

Check if each URL is reachable (HTTP HEAD):
```bash
python3 scripts/generate_youtube_thumbnails.py "<youtube-url>" --format markdown --check
```

Render the highest available thumbnail as a Markdown image:
```bash
python3 scripts/generate_youtube_thumbnails.py "<youtube-url>" --render-max-markdown
```

## Supported Inputs
- Full YouTube URLs (`youtube.com/watch?v=...`, `youtube.com/shorts/...`, `youtube.com/embed/...`)
- Short URLs (`youtu.be/...`)
- Raw video IDs (11 chars)

## Output Sizes
- `default` (120x90)
- `mqdefault` (320x180)
- `hqdefault` (480x360)
- `sddefault` (640x480)
- `maxresdefault` (1280x720, may be unavailable for some videos)

## Requirements
- Python 3.9+ (no third-party dependency)
