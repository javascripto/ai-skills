#!/usr/bin/env python3
"""Extract common YouTube video metadata using yt-dlp."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.parse
from datetime import datetime
from typing import Any

VIDEO_ID_PATTERN = re.compile(r"^[A-Za-z0-9_-]{11}$")


def extract_video_id(raw: str) -> str:
    value = raw.strip()
    if VIDEO_ID_PATTERN.match(value):
        return value

    parsed = urllib.parse.urlparse(value)
    host = parsed.netloc.lower().replace("www.", "")
    path = parsed.path.strip("/")

    if host == "youtu.be" and path:
        candidate = path.split("/")[0]
        if VIDEO_ID_PATTERN.match(candidate):
            return candidate

    if host in {"youtube.com", "m.youtube.com", "music.youtube.com"}:
        query = urllib.parse.parse_qs(parsed.query)
        if "v" in query and query["v"]:
            candidate = query["v"][0]
            if VIDEO_ID_PATTERN.match(candidate):
                return candidate

        segments = [segment for segment in path.split("/") if segment]
        if len(segments) >= 2 and segments[0] in {"shorts", "embed", "live"}:
            candidate = segments[1]
            if VIDEO_ID_PATTERN.match(candidate):
                return candidate

    raise ValueError(f"Unable to extract a valid YouTube video ID from: {raw}")


def ensure_url(input_value: str) -> str:
    try:
        video_id = extract_video_id(input_value)
        return f"https://www.youtube.com/watch?v={video_id}"
    except ValueError:
        return input_value.strip()


def format_duration_hms(seconds: int | None) -> str | None:
    if seconds is None or seconds < 0:
        return None
    hours, remainder = divmod(seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    if hours > 0:
        return f"{hours:02}:{minutes:02}:{secs:02}"
    return f"{minutes:02}:{secs:02}"


def format_upload_date(upload_date: str | None) -> str | None:
    if not upload_date:
        return None
    if len(upload_date) == 8 and upload_date.isdigit():
        dt = datetime.strptime(upload_date, "%Y%m%d")
        return dt.strftime("%Y-%m-%d")
    return upload_date


def run_yt_dlp(url: str) -> dict[str, Any]:
    cmd = [
        "yt-dlp",
        "--dump-single-json",
        "--skip-download",
        "--no-warnings",
        "--no-playlist",
        url,
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    except FileNotFoundError as exc:
        raise RuntimeError("yt-dlp not found. Install with: python3 -m pip install -U yt-dlp") from exc

    if result.returncode != 0:
        stderr = result.stderr.strip() or "unknown error"
        raise RuntimeError(f"yt-dlp failed: {stderr}")

    try:
        payload = json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError("failed to parse yt-dlp JSON output") from exc

    if not isinstance(payload, dict):
        raise RuntimeError("unexpected yt-dlp output type")
    return payload


def build_info(raw: dict[str, Any]) -> dict[str, Any]:
    duration_seconds = raw.get("duration")
    if isinstance(duration_seconds, float):
        duration_seconds = int(duration_seconds)
    if not isinstance(duration_seconds, int):
        duration_seconds = None

    tags = raw.get("tags") if isinstance(raw.get("tags"), list) else []
    categories = raw.get("categories") if isinstance(raw.get("categories"), list) else []

    return {
        "video_id": raw.get("id"),
        "title": raw.get("title"),
        "description": raw.get("description"),
        "channel": raw.get("channel"),
        "channel_id": raw.get("channel_id"),
        "channel_url": raw.get("channel_url"),
        "uploader": raw.get("uploader"),
        "uploader_id": raw.get("uploader_id"),
        "published_at": format_upload_date(raw.get("upload_date")),
        "duration_seconds": duration_seconds,
        "duration_hms": format_duration_hms(duration_seconds),
        "view_count": raw.get("view_count"),
        "like_count": raw.get("like_count"),
        "comment_count": raw.get("comment_count"),
        "tags": tags,
        "categories": categories,
        "thumbnail": raw.get("thumbnail"),
        "webpage_url": raw.get("webpage_url"),
    }


def cut_text(value: str | None, max_chars: int | None) -> str:
    if not value:
        return ""
    clean = value.strip()
    if max_chars is None or max_chars <= 0 or len(clean) <= max_chars:
        return clean
    if max_chars <= 3:
        return clean[:max_chars]
    return clean[: max_chars - 3].rstrip() + "..."


def print_plain(info: dict[str, Any], max_chars: int | None) -> None:
    print(f"video_id: {info.get('video_id')}")
    print(f"title: {info.get('title')}")
    print(f"channel: {info.get('channel')}")
    print(f"published_at: {info.get('published_at')}")
    print(f"duration_seconds: {info.get('duration_seconds')}")
    print(f"duration_hms: {info.get('duration_hms')}")
    print(f"views: {info.get('view_count')}")
    print(f"likes: {info.get('like_count')}")
    print(f"comments: {info.get('comment_count')}")
    print(f"webpage_url: {info.get('webpage_url')}")
    print(f"thumbnail: {info.get('thumbnail')}")

    tags = info.get("tags") or []
    categories = info.get("categories") or []
    print(f"tags: {', '.join(tags) if tags else '-'}")
    print(f"categories: {', '.join(categories) if categories else '-'}")
    print("description:")
    print(cut_text(info.get("description"), max_chars) or "-")


def print_markdown(info: dict[str, Any], max_chars: int | None) -> None:
    title = info.get("title") or "(untitled)"
    url = info.get("webpage_url") or ""
    title_line = f"## [{title}]({url})" if url else f"## {title}"
    print(title_line)
    print()
    print(f"- `video_id`: `{info.get('video_id')}`")
    print(f"- `channel`: {info.get('channel')}")
    print(f"- `published_at`: `{info.get('published_at')}`")
    print(f"- `duration`: `{info.get('duration_hms')}` ({info.get('duration_seconds')}s)")
    print(f"- `views`: `{info.get('view_count')}`")
    print(f"- `likes`: `{info.get('like_count')}`")
    print(f"- `comments`: `{info.get('comment_count')}`")
    print(f"- `thumbnail`: {info.get('thumbnail')}")

    tags = info.get("tags") or []
    categories = info.get("categories") or []
    print(f"- `tags`: {', '.join(tags) if tags else '-'}")
    print(f"- `categories`: {', '.join(categories) if categories else '-'}")
    print()
    print("### Description")
    print()
    print(cut_text(info.get("description"), max_chars) or "-")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract common YouTube video metadata from URL or video ID."
    )
    parser.add_argument("input", help="YouTube URL or raw video ID")
    parser.add_argument(
        "--format",
        choices=("markdown", "plain", "json"),
        default="markdown",
        help="Output format (default: markdown)",
    )
    parser.add_argument(
        "--description-max-chars",
        type=int,
        default=0,
        help="Max chars for description in plain/markdown output (0 = no limit)",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    target_url = ensure_url(args.input)
    max_chars = args.description_max_chars if args.description_max_chars > 0 else None

    try:
        raw = run_yt_dlp(target_url)
        info = build_info(raw)
    except Exception as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    if args.format == "json":
        print(json.dumps(info, indent=2, ensure_ascii=False))
    elif args.format == "plain":
        print_plain(info, max_chars)
    else:
        print_markdown(info, max_chars)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
