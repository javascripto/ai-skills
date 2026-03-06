---
name: local-faster-whisper-transcribe
description: Transcribe local audio/video files offline using faster-whisper, generating plain text and timestamped outputs without OpenAI API usage. Use when the user wants transcription with zero token cost, privacy-preserving local processing, or no API key dependency.
---

# Local Faster Whisper Transcribe

Use this skill for local-only transcription with `faster-whisper`.

## Quick start
```bash
python3 scripts/transcribe_local.py "path/to/audio-or-video.mp4" \
  --model small \
  --output-dir ./output/transcribe-local
```

## Workflow
1. Ensure `faster-whisper` is installed.
2. Run the bundled script on one or more local media files.
3. Read `.transcript.txt` for plain text and `.transcript.timed.txt` for timestamps.
4. If quality is low, rerun with a larger model (`medium` or `large-v3`).

## Commands
Single file:
```bash
python3 scripts/transcribe_local.py "./input/video.mp4" \
  --model small \
  --language pt \
  --output-dir ./output/transcribe-local
```

Multiple files:
```bash
python3 scripts/transcribe_local.py "./a.mp3" "./b.m4a" \
  --model small \
  --output-dir ./output/transcribe-local
```

## Outputs
For each input file `<name>`:
- `<name>.transcript.txt`
- `<name>.transcript.timed.txt`
- `<name>.transcript.json`

## Dependencies
Install Python package:
```bash
python3 -m pip install -U faster-whisper
```

Optional but recommended:
- `ffmpeg` for better media format compatibility.

## Notes
- This flow is local-only and does not use `OPENAI_API_KEY`.
- Use `--compute-type int8` by default for broad CPU compatibility.
