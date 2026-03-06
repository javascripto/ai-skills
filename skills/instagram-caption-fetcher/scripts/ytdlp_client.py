#!/usr/bin/env python3
from pathlib import Path
from typing import Any, Optional

from yt_dlp import YoutubeDL


def _cookie_tuple(browser: Optional[str]) -> Optional[tuple[str]]:
    if not browser:
        return None
    return (browser,)


def extract_metadata(url: str, cookies_from_browser: Optional[str] = None) -> dict[str, Any]:
    opts: dict[str, Any] = {
        "quiet": True,
        "no_warnings": True,
        "skip_download": True,
    }
    cookie_tuple = _cookie_tuple(cookies_from_browser)
    if cookie_tuple:
        opts["cookiesfrombrowser"] = cookie_tuple

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
    cookies_from_browser: Optional[str] = None,
) -> None:
    opts: dict[str, Any] = {
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

    cookie_tuple = _cookie_tuple(cookies_from_browser)
    if cookie_tuple:
        opts["cookiesfrombrowser"] = cookie_tuple

    with YoutubeDL(opts) as ydl:
        ydl.download([url])


def download_audio(
    url: str,
    output_dir: Path,
    cookies_from_browser: Optional[str] = None,
) -> None:
    opts: dict[str, Any] = {
        "quiet": True,
        "no_warnings": True,
        "format": "bestaudio/best",
        "outtmpl": str(output_dir / "%(id)s.audio.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "m4a",
                "preferredquality": "192",
            }
        ],
    }

    cookie_tuple = _cookie_tuple(cookies_from_browser)
    if cookie_tuple:
        opts["cookiesfrombrowser"] = cookie_tuple

    with YoutubeDL(opts) as ydl:
        ydl.download([url])


def find_latest_caption(output_dir: Path, video_id: str, extension: str) -> Optional[Path]:
    matches = sorted(output_dir.glob(f"{video_id}*.{extension}"), key=lambda p: p.stat().st_mtime)
    return matches[-1] if matches else None


def find_latest_audio(output_dir: Path, video_id: str) -> Optional[Path]:
    matches = sorted(output_dir.glob(f"{video_id}.audio.*"), key=lambda p: p.stat().st_mtime)
    return matches[-1] if matches else None
