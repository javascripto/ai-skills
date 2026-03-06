#!/usr/bin/env python3
import argparse
import json
import re
import sys
from pathlib import Path
from typing import Optional


def fail(msg: str, code: int = 1) -> None:
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(code)


def safe_stem(path: Path) -> str:
    stem = path.stem.strip() or "media"
    stem = re.sub(r"\s+", "_", stem)
    stem = re.sub(r"[^A-Za-z0-9._-]", "", stem)
    return stem or "media"


def fmt_ts(seconds: float) -> str:
    total_ms = int(round(seconds * 1000))
    hours, remainder = divmod(total_ms, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, ms = divmod(remainder, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02}.{ms:03}"


def transcribe_with_faster_whisper(
    media_file: Path,
    model_name: str,
    language: Optional[str],
    compute_type: str,
) -> tuple[str, list[tuple[float, float, str]]]:
    try:
        from faster_whisper import WhisperModel
    except ImportError as exc:
        raise RuntimeError("faster-whisper is not installed") from exc

    model = WhisperModel(model_name, device="auto", compute_type=compute_type)
    segments_iter, _ = model.transcribe(str(media_file), language=language, vad_filter=True)

    text_parts: list[str] = []
    segments: list[tuple[float, float, str]] = []
    for seg in segments_iter:
        seg_text = (seg.text or "").strip()
        if not seg_text:
            continue
        start = float(seg.start)
        end = float(seg.end)
        segments.append((start, end, seg_text))
        text_parts.append(seg_text)

    return " ".join(text_parts).strip(), segments


def write_outputs(output_dir: Path, base_name: str, text: str, segments: list[tuple[float, float, str]]) -> None:
    transcript_file = output_dir / f"{base_name}.transcript.txt"
    transcript_file.write_text((text.strip() + "\n") if text.strip() else "", encoding="utf-8")

    timed_file = output_dir / f"{base_name}.transcript.timed.txt"
    timed_lines = [f"[{fmt_ts(start)} --> {fmt_ts(end)}] {seg_text}" for start, end, seg_text in segments]
    timed_file.write_text(("\n".join(timed_lines).strip() + "\n") if timed_lines else "", encoding="utf-8")

    json_file = output_dir / f"{base_name}.transcript.json"
    payload = {
        "text": text,
        "segments": [
            {"start": start, "end": end, "text": seg_text} for start, end, seg_text in segments
        ],
    }
    json_file.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"transcript_file={transcript_file}")
    print(f"transcript_timed_file={timed_file}")
    print(f"transcript_json_file={json_file}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Transcribe local audio/video files with faster-whisper (offline/local-only)."
    )
    parser.add_argument("media", nargs="+", help="Path(s) to local audio/video files")
    parser.add_argument("--model", default="small", help="faster-whisper model (tiny/base/small/medium/large-v3)")
    parser.add_argument("--language", default=None, help="Language hint (e.g. pt, en). Omit for auto-detect.")
    parser.add_argument("--compute-type", default="int8", help="Whisper compute type (default: int8)")
    parser.add_argument("--output-dir", default=".", help="Directory for output transcript files")
    args = parser.parse_args()

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    had_error = False
    for raw in args.media:
        media_file = Path(raw).expanduser().resolve()
        if not media_file.exists() or not media_file.is_file():
            print(f"ERROR: input file not found: {media_file}", file=sys.stderr)
            had_error = True
            continue

        base_name = safe_stem(media_file)
        print(f"input_file={media_file}")
        try:
            text, segments = transcribe_with_faster_whisper(
                media_file=media_file,
                model_name=args.model,
                language=args.language,
                compute_type=args.compute_type,
            )
        except Exception as exc:  # noqa: BLE001
            print(f"ERROR: transcription failed for {media_file}: {exc}", file=sys.stderr)
            had_error = True
            continue

        if not text:
            print(f"ERROR: empty transcription for {media_file}", file=sys.stderr)
            had_error = True
            continue

        write_outputs(output_dir=output_dir, base_name=base_name, text=text, segments=segments)

    if had_error:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
