#!/usr/bin/env python3
import subprocess
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


def caption_keys(subs: dict[str, Any]) -> list[str]:
    # yt-dlp can expose live chat as a "subtitle" track, but that is not a
    # useful caption source for summarization. Keep it out of the selection
    # flow so we only choose real subtitles / auto-captions.
    return [key for key in subs.keys() if key.strip().lower().replace("_", "-") != "live-chat"]


def download_subtitles(
    url: str,
    output_dir: Path,
    lang: str,
    source: str,
    caption_format: str,
) -> None:
    cmd = [
        "yt-dlp",
        "--skip-download",
        "--sub-langs",
        lang,
        "-o",
        str(output_dir / "%(title)s [%(id)s].%(ext)s"),
    ]
    if source == "manual":
        cmd.append("--write-subs")
    else:
        cmd.append("--write-auto-subs")
    if caption_format == "srt":
        cmd.append("--convert-subs")
        cmd.append("srt")

    subprocess.run(cmd + [url], check=True)


def find_latest_caption(output_dir: Path, video_id: str, extension: str) -> Optional[Path]:
    matches = sorted(output_dir.glob(f"*{video_id}*.{extension}"), key=lambda p: p.stat().st_mtime)
    if not matches:
        matches = sorted(output_dir.glob(f"*.{extension}"), key=lambda p: p.stat().st_mtime)
    return matches[-1] if matches else None
