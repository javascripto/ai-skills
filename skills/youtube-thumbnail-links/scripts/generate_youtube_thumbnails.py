#!/usr/bin/env python3
"""Generate YouTube thumbnail URLs from a video URL or video ID."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request

THUMBNAILS = [
    ("default", "120x90"),
    ("mqdefault", "320x180"),
    ("hqdefault", "480x360"),
    ("sddefault", "640x480"),
    ("maxresdefault", "1280x720"),
]
THUMBNAILS_DESC = list(reversed(THUMBNAILS))

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


def thumbnail_url(video_id: str, key: str) -> str:
    return f"https://img.youtube.com/vi/{video_id}/{key}.jpg"


def check_url(url: str, timeout: float = 4.0) -> bool:
    request = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return 200 <= getattr(response, "status", 0) < 400
    except Exception:
        return False


def build_rows(video_id: str, do_check: bool) -> list[dict[str, str | bool]]:
    rows: list[dict[str, str | bool]] = []
    for key, size in THUMBNAILS:
        url = thumbnail_url(video_id, key)
        row: dict[str, str | bool] = {"name": key, "size": size, "url": url}
        if do_check:
            row["available"] = check_url(url)
        rows.append(row)
    return rows


def find_best_thumbnail(video_id: str) -> dict[str, str]:
    for key, size in THUMBNAILS_DESC:
        url = thumbnail_url(video_id, key)
        if check_url(url):
            return {"name": key, "size": size, "url": url}
    raise RuntimeError("No reachable thumbnail URL found for this video.")


def print_plain(rows: list[dict[str, str | bool]]) -> None:
    for row in rows:
        line = f"{row['name']} ({row['size']}): {row['url']}"
        if "available" in row:
            suffix = "OK" if row["available"] else "unavailable"
            line = f"{line} [{suffix}]"
        print(line)


def print_markdown(rows: list[dict[str, str | bool]]) -> None:
    for row in rows:
        label = f"{row['name']} ({row['size']})"
        if row["name"] == "maxresdefault":
            label = f"{label}, if available"
        line = f"- [{label}]({row['url']})"
        if "available" in row:
            suffix = "OK" if row["available"] else "unavailable"
            line = f"{line} `{suffix}`"
        print(line)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate YouTube thumbnail URLs from a URL or video ID."
    )
    parser.add_argument("input", help="YouTube URL or raw video ID")
    parser.add_argument(
        "--format",
        choices=("markdown", "plain", "json"),
        default="markdown",
        help="Output format (default: markdown)",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Check URL reachability with HTTP HEAD",
    )
    parser.add_argument(
        "--render-max-markdown",
        action="store_true",
        help="Render only the highest available thumbnail as Markdown image",
    )
    parser.add_argument(
        "--with-max-image",
        action="store_true",
        help="When using --format markdown, append the highest available thumbnail as Markdown image",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        video_id = extract_video_id(args.input)
    except ValueError as exc:
        print(f"[ERROR] {exc}", file=sys.stderr)
        return 1

    if args.render_max_markdown:
        try:
            best = find_best_thumbnail(video_id)
        except RuntimeError as exc:
            print(f"[ERROR] {exc}", file=sys.stderr)
            return 2
        alt = f"YouTube thumbnail {best['name']} ({best['size']})"
        print(f"![{alt}]({best['url']})")
        return 0

    rows = build_rows(video_id, args.check)
    if args.format == "json":
        print(json.dumps({"video_id": video_id, "thumbnails": rows}, indent=2))
    elif args.format == "plain":
        print_plain(rows)
    else:
        print_markdown(rows)
        if args.with_max_image:
            try:
                best = find_best_thumbnail(video_id)
            except RuntimeError as exc:
                print(f"[ERROR] {exc}", file=sys.stderr)
                return 2
            alt = f"YouTube thumbnail {best['name']} ({best['size']})"
            print()
            print(f"![{alt}]({best['url']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
