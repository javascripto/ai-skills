#!/usr/bin/env python3
from pathlib import Path
from typing import Any, Optional

from yt_dlp import YoutubeDL


def extract_metadata(url: str) -> dict[str, Any]:
    opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
    }
    with YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=False)
    if not isinstance(info, dict):
        raise RuntimeError("failed to extract video metadata")
    return info


def download_subtitles(
    url: str,
    output_dir: Path,
    lang: str,
    source: str,
    caption_format: str,
) -> None:
    opts = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
        "outtmpl": str(output_dir / "%(id)s.%(language)s.%(ext)s"),
        "subtitleslangs": [lang],
        "subtitlesformat": "vtt",
        "writesubtitles": source == "manual",
        "writeautomaticsub": source == "auto",
    }
    if caption_format == "srt":
        opts["convertsubtitles"] = "srt"

    with YoutubeDL(opts) as ydl:
        ydl.download([url])


def find_latest_caption(output_dir: Path, video_id: str, extension: str) -> Optional[Path]:
    matches = sorted(output_dir.glob(f"{video_id}*.{extension}"), key=lambda p: p.stat().st_mtime)
    return matches[-1] if matches else None
