---
name: youtube-caption-fetcher
description: Fetch YouTube captions with timestamps in original language or Brazilian Portuguese (`pt-BR`) using `yt-dlp` and fallback to auto-captions. Use for video analysis/summarization from subtitles without running full audio transcription.
---

# Youtube Caption Fetcher

Use `yt-dlp` via Python script for fast subtitle-first workflows.

## Path 1: Captions First
```bash
python3 scripts/fetch_youtube_captions.py "<youtube-url>" \
  --mode pt-br \
  --format srt \
  --output-dir ./captions \
  --timed-text
```

## Arquivos de saída gerados
- `caption_file`: arquivo principal de legenda (`.srt` ou `.vtt`) no `--output-dir`
- `timed_text_file` (quando `--timed-text`): `<nome>.timed.txt` com formato `[start --> end] texto`
- `timed_text_clean_file` (quando `--timed-text`): `<nome>.timed.clean.txt` com parciais/duplicatas adjacentes consolidadas
- Se `.srt` não estiver disponível para a fonte, o `caption_file` cai automaticamente para `.vtt`

Fallback logic:
- `original`: original language -> first manual -> first auto-caption
- `pt-br`: `pt-BR`/`pt` -> English -> first manual/auto-caption

## Requirements
- Install Python package `yt-dlp` (`python3 -m pip install -U yt-dlp`).
- Allow network access to YouTube when running the script.
