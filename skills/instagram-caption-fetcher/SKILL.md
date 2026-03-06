---
name: instagram-caption-fetcher
description: Fetch captions from Instagram video URLs (Reels/posts) using yt-dlp, with fallback to audio transcription when subtitles are missing. Use when the user needs timestamps, transcript extraction, or caption files from Instagram videos for analysis, summarization, or translation.
---

# Instagram Caption Fetcher

Prefer a two-step pipeline: try embedded captions first, then transcribe audio.

## Quick start
```bash
python3 scripts/instagram_caption_pipeline.py "<instagram-url>" \
  --mode original \
  --format srt \
  --output-dir ./captions \
  --timed-text
```

## Recommended workflow
1. Run caption-first flow (default).
2. If Instagram has no subtitle tracks, let the script auto-fallback to transcription.
3. If the user explicitly wants transcription even with captions, add `--force-transcribe`.
4. For private/auth-required content, pass cookies via `--cookies-from-browser`.

## Decision rules
- Default `--mode original` to keep source language.
- Use `--mode pt-br` when the user asks for Portuguese-first subtitles.
- Keep `--transcribe-engine faster-whisper` (local-only, no token cost).
- Use model `small` by default; switch to `medium` or `large-v3` for harder audio.
- Use [$local-faster-whisper-transcribe](../local-faster-whisper-transcribe/SKILL.md) when the user asks for standalone local transcription.

## Outputs
- `caption_file`: primary caption file (`.srt` or `.vtt`) when subtitle tracks exist.
- `timed_text_file`: plain text `[start --> end] text` generated from caption file.
- `timed_text_clean_file`: deduplicated timed text (helps with auto-caption partials).
- `audio_file`: downloaded audio used for transcription fallback.
- `transcript_file`: plain transcript generated from audio.
- `transcript_timed_file`: timed transcript `[start --> end] text` from transcription segments.

## Commands
Caption-first with auto transcription fallback:
```bash
python3 scripts/instagram_caption_pipeline.py "<instagram-url>" \
  --mode original \
  --format srt \
  --output-dir ./captions \
  --timed-text
```

Force transcription (ignore available subtitle tracks):
```bash
python3 scripts/instagram_caption_pipeline.py "<instagram-url>" \
  --force-transcribe \
  --transcribe-engine faster-whisper \
  --faster-whisper-model small \
  --output-dir ./captions
```

Authenticated fetch using browser cookies:
```bash
python3 scripts/instagram_caption_pipeline.py "<instagram-url>" \
  --cookies-from-browser chrome \
  --output-dir ./captions
```

## Dependencies
Install base dependency:
```bash
python3 -m pip install -U yt-dlp
```

For local transcription fallback:
```bash
python3 -m pip install -U faster-whisper
```

Optional system dependency (recommended for broader audio format support):
- `ffmpeg`

## Notes
- Instagram frequently provides no subtitle tracks; fallback transcription is expected behavior.
- Some Instagram URLs require authentication cookies to download media metadata/audio.
- Do not assume perfect punctuation in auto transcription; review final text for publishing.
