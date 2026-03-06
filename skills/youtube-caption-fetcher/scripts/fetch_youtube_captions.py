#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path
from typing import Iterable, Optional

from ytdlp_client import download_subtitles, extract_metadata, find_latest_caption


def fail(msg: str, code: int = 1) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(code)


def normalize_lang(lang: str) -> str:
    return lang.strip().lower().replace("_", "-")


def find_lang_key(available: Iterable[str], wanted: Iterable[str]) -> Optional[str]:
    normalized = {normalize_lang(k): k for k in available}
    for candidate in wanted:
        key = normalized.get(normalize_lang(candidate))
        if key:
            return key
    return None


def original_lang_candidates(video_lang: Optional[str]) -> list[str]:
    if not video_lang:
        return []
    norm = normalize_lang(video_lang)
    parts = norm.split("-")
    short = parts[0]
    candidates = [video_lang, norm, short]
    if short == "pt":
        candidates.extend(["pt-br", "pt-pt"])
    return list(dict.fromkeys(candidates))


def ptbr_candidates() -> list[str]:
    return ["pt-BR", "pt-br", "pt", "pt-PT", "pt-pt"]


def pick_language(
    mode: str,
    video_lang: Optional[str],
    manual_subs: dict,
    auto_subs: dict,
) -> tuple[str, str]:
    manual_keys = list(manual_subs.keys())
    auto_keys = list(auto_subs.keys())

    if mode == "pt-br":
        wanted = ptbr_candidates()
    else:
        wanted = original_lang_candidates(video_lang)

    if wanted:
        manual_match = find_lang_key(manual_keys, wanted)
        if manual_match:
            return manual_match, "manual"

        auto_match = find_lang_key(auto_keys, wanted)
        if auto_match:
            return auto_match, "auto"

    if mode == "original":
        if manual_keys:
            return sorted(manual_keys)[0], "manual"
        if auto_keys:
            return sorted(auto_keys)[0], "auto"
    else:
        fallback = ["en", "en-US", "en-GB"]
        manual_match = find_lang_key(manual_keys, fallback)
        if manual_match:
            return manual_match, "manual"
        auto_match = find_lang_key(auto_keys, fallback)
        if auto_match:
            return auto_match, "auto"
        if manual_keys:
            return sorted(manual_keys)[0], "manual"
        if auto_keys:
            return sorted(auto_keys)[0], "auto"

    fail("no subtitles or auto-captions found for this video")
    raise AssertionError("unreachable")


TIMESTAMP_LINE = re.compile(
    r"^(\d{2}:\d{2}:\d{2}[.,]\d{3}|\d{2}:\d{2}[.,]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[.,]\d{3}|\d{2}:\d{2}[.,]\d{3})"
)


def caption_to_timed_text(caption_path: Path, text_path: Path) -> None:
    lines = caption_path.read_text(encoding="utf-8", errors="replace").splitlines()
    output: list[str] = []
    current_time = ""
    current_text: list[str] = []

    def flush() -> None:
        nonlocal current_time, current_text
        if current_time and current_text:
            joined = " ".join(part.strip() for part in current_text if part.strip())
            joined = re.sub(r"\s+", " ", joined).strip()
            if joined:
                output.append(f"[{current_time}] {joined}")
        current_time = ""
        current_text = []

    for raw in lines:
        line = raw.strip()
        if not line or line == "WEBVTT" or line.isdigit():
            if not line:
                flush()
            continue
        if line.startswith("NOTE ") or line.startswith("STYLE") or line.startswith("REGION"):
            continue

        ts = TIMESTAMP_LINE.match(line)
        if ts:
            flush()
            start, end = ts.groups()
            current_time = f"{start} --> {end}"
            continue

        if line.startswith("<"):
            continue
        current_text.append(re.sub(r"<[^>]+>", "", line))

    flush()
    text_path.write_text("\n".join(output).strip() + "\n", encoding="utf-8")


def find_downloaded_caption(output_dir: Path, video_id: str, extension: str) -> Path:
    match = find_latest_caption(output_dir, video_id, extension)
    if match:
        return match

    # Some videos/caption sources do not convert cleanly to SRT.
    # Fallback to the original VTT so the workflow still succeeds.
    if extension == "srt":
        fallback_match = find_latest_caption(output_dir, video_id, "vtt")
        if fallback_match:
            return fallback_match

    fail(f"caption file not found after download in {output_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Fetch YouTube captions (manual or auto) with timestamps using yt-dlp."
    )
    parser.add_argument("url", help="YouTube video URL")
    parser.add_argument(
        "--mode",
        choices=["original", "pt-br"],
        default="original",
        help="Try original video language or Brazilian Portuguese",
    )
    parser.add_argument(
        "--format",
        choices=["srt", "vtt"],
        default="srt",
        dest="caption_format",
        help="Caption file format",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Folder where caption files will be written",
    )
    parser.add_argument(
        "--timed-text",
        action="store_true",
        help="Also generate a plain text file preserving each caption timestamp",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        metadata = extract_metadata(args.url)
    except Exception as exc:
        fail(str(exc))

    video_id = metadata.get("id")
    if not video_id:
        fail("could not resolve video id")

    video_lang = metadata.get("language")
    manual_subs = metadata.get("subtitles") or {}
    auto_subs = metadata.get("automatic_captions") or {}

    selected_lang, source = pick_language(args.mode, video_lang, manual_subs, auto_subs)

    try:
        download_subtitles(
            url=args.url,
            output_dir=output_dir,
            lang=selected_lang,
            source=source,
            caption_format=args.caption_format,
        )
    except Exception as exc:
        fail(str(exc))

    caption_file = find_downloaded_caption(output_dir, video_id, args.caption_format)
    if caption_file.suffix != f".{args.caption_format}":
        print(
            f"warning=requested format .{args.caption_format} unavailable; using {caption_file.suffix} fallback"
        )
    print(f"caption_file={caption_file}")
    print(f"mode={args.mode}")
    print(f"source={source}")
    print(f"language={selected_lang}")

    if args.timed_text:
        text_file = caption_file.with_suffix(".timed.txt")
        caption_to_timed_text(caption_file, text_file)
        print(f"timed_text_file={text_file}")


if __name__ == "__main__":
    main()
