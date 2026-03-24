#!/usr/bin/env python3
"""Transcribe local audio/video files using whisper.cpp (whisper-cli)."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
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


def find_whisper_cli() -> str:
    """Locate the whisper-cli binary."""
    for name in ("whisper-cli", "whisper-cpp", "whisper"):
        found = shutil.which(name)
        if found:
            return found
    fail(
        "whisper-cli not found in PATH. Install with:\n"
        "  brew install whisper-cpp        (macOS)\n"
        "  pip install whisper.cpp-cli     (cross-platform)\n"
        "  or build from source: https://github.com/ggml-org/whisper.cpp"
    )
    raise AssertionError("unreachable")


def convert_to_wav(input_path: Path, tmp_dir: Path) -> Path:
    """Convert any audio/video to 16kHz mono WAV via ffmpeg."""
    wav_path = tmp_dir / f"{safe_stem(input_path)}.wav"
    cmd = [
        "ffmpeg", "-y", "-i", str(input_path),
        "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le",
        str(wav_path),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, check=False)
    if result.returncode != 0:
        fail(f"ffmpeg conversion failed for {input_path}: {result.stderr.strip()}")
    return wav_path


NATIVE_FORMATS = {".flac", ".mp3", ".ogg", ".wav"}


def needs_conversion(path: Path, force_wav: bool) -> bool:
    if force_wav:
        return True
    return path.suffix.lower() not in NATIVE_FORMATS


def fmt_ts(seconds: float) -> str:
    total_ms = int(round(seconds * 1000))
    hours, remainder = divmod(total_ms, 3_600_000)
    minutes, remainder = divmod(remainder, 60_000)
    secs, ms = divmod(remainder, 1000)
    return f"{hours:02}:{minutes:02}:{secs:02}.{ms:03}"


TIMESTAMP_RE = re.compile(
    r"^\[(\d{2}:\d{2}:\d{2}\.\d{3})\s*-->\s*(\d{2}:\d{2}:\d{2}\.\d{3})\]\s*(.+)$"
)


def parse_whisper_stdout(stdout: str) -> tuple[str, list[tuple[str, str, str]]]:
    """Parse whisper-cli stdout which has lines like:
    [00:00:00.000 --> 00:00:03.520]  Hello world
    """
    segments: list[tuple[str, str, str]] = []
    text_parts: list[str] = []

    for line in stdout.splitlines():
        line = line.strip()
        match = TIMESTAMP_RE.match(line)
        if match:
            start, end, text = match.groups()
            text = text.strip()
            if text:
                segments.append((start, end, text))
                text_parts.append(text)

    return " ".join(text_parts).strip(), segments


def ts_to_seconds(ts: str) -> float:
    """Convert HH:MM:SS.mmm to float seconds."""
    parts = ts.split(":")
    hours = int(parts[0])
    minutes = int(parts[1])
    sec_ms = parts[2].split(".")
    secs = int(sec_ms[0])
    ms = int(sec_ms[1]) if len(sec_ms) > 1 else 0
    return hours * 3600 + minutes * 60 + secs + ms / 1000.0


def write_outputs(
    output_dir: Path,
    base_name: str,
    text: str,
    segments: list[tuple[str, str, str]],
) -> None:
    # Plain text transcript
    transcript_file = output_dir / f"{base_name}.transcript.txt"
    transcript_file.write_text(
        (text.strip() + "\n") if text.strip() else "", encoding="utf-8"
    )

    # Timed text
    timed_file = output_dir / f"{base_name}.transcript.timed.txt"
    timed_lines = [f"[{start} --> {end}] {seg_text}" for start, end, seg_text in segments]
    timed_file.write_text(
        ("\n".join(timed_lines).strip() + "\n") if timed_lines else "", encoding="utf-8"
    )

    # JSON
    json_file = output_dir / f"{base_name}.transcript.json"
    payload = {
        "text": text,
        "segments": [
            {
                "start": ts_to_seconds(start),
                "end": ts_to_seconds(end),
                "text": seg_text,
            }
            for start, end, seg_text in segments
        ],
    }
    json_file.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(f"transcript_file={transcript_file}")
    print(f"transcript_timed_file={timed_file}")
    print(f"transcript_json_file={json_file}")


def run_whisper_cli(
    whisper_bin: str,
    model_path: Path,
    audio_file: Path,
    output_dir: Path,
    base_name: str,
    language: Optional[str],
    threads: int,
    no_gpu: bool,
) -> str:
    """Run whisper-cli and return its stdout."""
    srt_prefix = str(output_dir / base_name)

    cmd = [
        whisper_bin,
        "-m", str(model_path),
        "-f", str(audio_file),
        "-t", str(threads),
        "-osrt",
        "-of", srt_prefix,
    ]
    if language:
        cmd.extend(["-l", language])
    if no_gpu:
        cmd.append("-ng")

    result = subprocess.run(cmd, capture_output=True, text=True, check=False)

    if result.returncode != 0:
        stderr = result.stderr.strip() or "unknown error"
        fail(f"whisper-cli failed: {stderr}")

    srt_path = Path(f"{srt_prefix}.srt")
    if srt_path.exists():
        print(f"srt_file={srt_path}")

    return result.stdout


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Transcribe local audio/video files with whisper.cpp (whisper-cli)."
    )
    parser.add_argument("media", nargs="+", help="Path(s) to local audio/video files")
    parser.add_argument(
        "--model-path",
        required=True,
        help="Path to GGML model file (e.g. ~/models/ggml-small.bin)",
    )
    parser.add_argument(
        "--language",
        default=None,
        help="Language hint (e.g. pt, en). Omit for auto-detect.",
    )
    parser.add_argument(
        "--threads",
        type=int,
        default=4,
        help="Number of CPU threads (default: 4)",
    )
    parser.add_argument(
        "--force-wav",
        action="store_true",
        help="Always convert input to 16kHz WAV before transcription",
    )
    parser.add_argument(
        "--output-dir",
        default=".",
        help="Directory for output transcript files",
    )
    parser.add_argument(
        "--no-gpu",
        action="store_true",
        help="Disable GPU/Metal and run on CPU only",
    )
    args = parser.parse_args()

    model_path = Path(args.model_path).expanduser().resolve()
    if not model_path.exists():
        fail(f"model file not found: {model_path}")

    output_dir = Path(args.output_dir).expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    whisper_bin = find_whisper_cli()
    print(f"whisper_bin={whisper_bin}")

    had_error = False
    for raw in args.media:
        media_file = Path(raw).expanduser().resolve()
        if not media_file.exists() or not media_file.is_file():
            print(f"ERROR: input file not found: {media_file}", file=sys.stderr)
            had_error = True
            continue

        base_name = safe_stem(media_file)
        print(f"input_file={media_file}")

        # Convert if needed
        tmp_dir_obj = None
        audio_input = media_file
        if needs_conversion(media_file, args.force_wav):
            tmp_dir_obj = tempfile.TemporaryDirectory()
            audio_input = convert_to_wav(media_file, Path(tmp_dir_obj.name))
            print(f"converted_wav={audio_input}")

        try:
            stdout = run_whisper_cli(
                whisper_bin=whisper_bin,
                model_path=model_path,
                audio_file=audio_input,
                output_dir=output_dir,
                base_name=base_name,
                language=args.language,
                threads=args.threads,
                no_gpu=args.no_gpu,
            )
        except SystemExit:
            had_error = True
            continue
        finally:
            if tmp_dir_obj:
                tmp_dir_obj.cleanup()

        text, segments = parse_whisper_stdout(stdout)

        if not text:
            print(f"ERROR: empty transcription for {media_file}", file=sys.stderr)
            had_error = True
            continue

        write_outputs(
            output_dir=output_dir,
            base_name=base_name,
            text=text,
            segments=segments,
        )

    if had_error:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
