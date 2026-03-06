#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Iterable, Optional

from ytdlp_client import (
    download_audio,
    download_subtitles,
    extract_metadata,
    find_latest_audio,
    find_latest_caption,
)


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
    short = norm.split("-")[0]
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
) -> Optional[tuple[str, str]]:
    manual_keys = list(manual_subs.keys())
    auto_keys = list(auto_subs.keys())

    wanted = ptbr_candidates() if mode == "pt-br" else original_lang_candidates(video_lang)

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

    return None


TIMESTAMP_LINE = re.compile(
    r"^(\d{2}:\d{2}:\d{2}[.,]\d{3}|\d{2}:\d{2}[.,]\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}[.,]\d{3}|\d{2}:\d{2}[.,]\d{3})"
)
TIMED_TXT_LINE = re.compile(r"^\[(.+?)\]\s*(.+)$")


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


def normalize_text_for_compare(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def clean_partial_duplicates(input_path: Path, output_path: Path) -> None:
    lines = input_path.read_text(encoding="utf-8", errors="replace").splitlines()
    kept: list[tuple[str, str]] = []

    for raw in lines:
        line = raw.strip()
        if not line:
            continue
        parsed = TIMED_TXT_LINE.match(line)
        if not parsed:
            continue

        timerange, text = parsed.groups()
        norm = normalize_text_for_compare(text)
        if not norm:
            continue

        if not kept:
            kept.append((timerange, text))
            continue

        _, prev_text = kept[-1]
        prev_norm = normalize_text_for_compare(prev_text)

        if norm == prev_norm:
            continue
        if norm in prev_norm:
            continue
        if prev_norm in norm:
            kept[-1] = (timerange, text)
            continue

        kept.append((timerange, text))

    output = [f"[{timerange}] {text}" for timerange, text in kept]
    output_path.write_text("\n".join(output).strip() + "\n", encoding="utf-8")


def fmt_ts(seconds: float) -> str:
    total_ms = int(round(seconds * 1000))
    hours, remainder = divmod(total_ms, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, ms = divmod(remainder, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02}.{ms:03}"


def write_transcription_outputs(
    output_dir: Path,
    base_name: str,
    text: str,
    segments: list[tuple[float, float, str]],
) -> tuple[Path, Optional[Path], Path]:
    transcript_file = output_dir / f"{base_name}.transcript.txt"
    transcript_file.write_text(text.strip() + "\n", encoding="utf-8")

    timed_file: Optional[Path] = None
    if segments:
        timed_file = output_dir / f"{base_name}.transcript.timed.txt"
        lines = [f"[{fmt_ts(start)} --> {fmt_ts(end)}] {seg_text}" for start, end, seg_text in segments]
        timed_file.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")

    json_file = output_dir / f"{base_name}.transcript.json"
    json_file.write_text(
        json.dumps(
            {
                "text": text,
                "segments": [
                    {"start": start, "end": end, "text": seg_text} for start, end, seg_text in segments
                ],
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return transcript_file, timed_file, json_file


def transcribe_with_faster_whisper(
    audio_file: Path,
    model_name: str,
    language: Optional[str],
) -> tuple[str, list[tuple[float, float, str]]]:
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise RuntimeError("faster-whisper is not installed") from exc

    model = WhisperModel(model_name, device="auto", compute_type="int8")
    segments_iter, _ = model.transcribe(str(audio_file), language=language, vad_filter=True)

    segments: list[tuple[float, float, str]] = []
    parts: list[str] = []
    for seg in segments_iter:
        seg_text = (seg.text or "").strip()
        if not seg_text:
            continue
        segments.append((float(seg.start), float(seg.end), seg_text))
        parts.append(seg_text)

    text = " ".join(parts).strip()
    return text, segments


def transcribe_audio(
    engine: str,
    audio_file: Path,
    faster_whisper_model: str,
    language: Optional[str],
) -> tuple[str, str, list[tuple[float, float, str]]]:
    if engine == "none":
        raise RuntimeError("transcription disabled by --transcribe-engine none")

    text, segments = transcribe_with_faster_whisper(audio_file, faster_whisper_model, language)
    return "faster-whisper", text, segments


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Fetch captions from Instagram via yt-dlp and fallback to audio transcription when subtitles are missing."
        )
    )
    parser.add_argument("url", help="Instagram video URL (reel/post)")
    parser.add_argument(
        "--mode",
        choices=["original", "pt-br"],
        default="original",
        help="Preferred subtitle language strategy",
    )
    parser.add_argument(
        "--format",
        choices=["srt", "vtt"],
        default="srt",
        dest="caption_format",
        help="Caption file format",
    )
    parser.add_argument("--output-dir", default=".", help="Folder where files are written")
    parser.add_argument(
        "--timed-text",
        action="store_true",
        help="Generate timed text files from caption tracks",
    )
    parser.add_argument(
        "--force-transcribe",
        action="store_true",
        help="Transcribe audio even if captions were found",
    )
    parser.add_argument(
        "--transcribe-engine",
        choices=["faster-whisper", "none"],
        default="faster-whisper",
        help="Transcription backend for fallback mode",
    )
    parser.add_argument(
        "--faster-whisper-model",
        default="small",
        help="Model name for faster-whisper backend",
    )
    parser.add_argument(
        "--language",
        default=None,
        help="Optional language hint for transcription (e.g. en, pt)",
    )
    parser.add_argument(
        "--cookies-from-browser",
        default=None,
        help="Browser name for yt-dlp cookies (e.g. chrome, firefox, safari)",
    )
    args = parser.parse_args()

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    try:
        metadata = extract_metadata(args.url, cookies_from_browser=args.cookies_from_browser)
    except Exception as exc:  # noqa: BLE001
        fail(str(exc))

    video_id = metadata.get("id")
    if not video_id:
        fail("could not resolve video id")

    video_lang = metadata.get("language")
    manual_subs = metadata.get("subtitles") or {}
    auto_subs = metadata.get("automatic_captions") or {}

    caption_file: Optional[Path] = None
    selected_lang = ""
    source = ""

    if not args.force_transcribe:
        selection = pick_language(args.mode, video_lang, manual_subs, auto_subs)
        if selection:
            selected_lang, source = selection
            try:
                download_subtitles(
                    url=args.url,
                    output_dir=output_dir,
                    lang=selected_lang,
                    source=source,
                    caption_format=args.caption_format,
                    cookies_from_browser=args.cookies_from_browser,
                )
                caption_file = find_latest_caption(output_dir, video_id, args.caption_format)
                if not caption_file and args.caption_format == "srt":
                    caption_file = find_latest_caption(output_dir, video_id, "vtt")
            except Exception as exc:  # noqa: BLE001
                print(f"warning=subtitle download failed: {exc}")

    if caption_file:
        print(f"caption_file={caption_file}")
        print(f"mode={args.mode}")
        print(f"source={source}")
        print(f"language={selected_lang}")
        if args.timed_text:
            text_file = caption_file.with_suffix(".timed.txt")
            caption_to_timed_text(caption_file, text_file)
            print(f"timed_text_file={text_file}")
            clean_file = caption_file.with_suffix(".timed.clean.txt")
            clean_partial_duplicates(text_file, clean_file)
            print(f"timed_text_clean_file={clean_file}")
    else:
        print("caption_file=")
        print("subtitle_status=not_found")

    should_transcribe = args.force_transcribe or not caption_file
    if not should_transcribe:
        return

    if args.transcribe_engine == "none":
        if caption_file:
            return
        fail("no subtitle tracks found and transcription is disabled")

    try:
        download_audio(args.url, output_dir=output_dir, cookies_from_browser=args.cookies_from_browser)
    except Exception as exc:  # noqa: BLE001
        fail(f"audio download failed: {exc}")

    audio_file = find_latest_audio(output_dir, video_id)
    if not audio_file:
        fail("audio file not found after download")

    try:
        used_engine, text, segments = transcribe_audio(
            engine=args.transcribe_engine,
            audio_file=audio_file,
            faster_whisper_model=args.faster_whisper_model,
            language=args.language,
        )
    except Exception as exc:  # noqa: BLE001
        fail(f"transcription failed: {exc}")

    if not text:
        fail("transcription returned empty text")

    transcript_file, transcript_timed_file, transcript_json_file = write_transcription_outputs(
        output_dir=output_dir,
        base_name=video_id,
        text=text,
        segments=segments,
    )

    print(f"audio_file={audio_file}")
    print(f"transcribe_engine={used_engine}")
    print(f"transcript_file={transcript_file}")
    print(f"transcript_json_file={transcript_json_file}")
    if transcript_timed_file:
        print(f"transcript_timed_file={transcript_timed_file}")


if __name__ == "__main__":
    main()
