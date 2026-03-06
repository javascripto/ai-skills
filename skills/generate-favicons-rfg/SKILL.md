---
name: generate-favicons-rfg
description: Generate favicon/icon packs and manifest artifacts from a user-provided base icon through RealFaviconGenerator and integrate them safely into existing web projects by updating index.html references without destructive overwrites. Use when asked to create, refresh, or fix favicon files (`favicon.ico`, PNG/SVG icons, `site.webmanifest`) and wire head tags automatically, especially in Vite + React + TypeScript projects.
---

# Generate Favicons RFG

Generate favicon artifacts through RealFaviconGenerator with browser automation, then integrate references into the project in an idempotent way.

## Prerequisites
- Ensure `python3` is available.
- Ensure Playwright CLI wrapper is available via `$PWCLI` or at `$CODEX_HOME/skills/playwright/scripts/playwright_cli.sh`.
- Provide an input icon (`.svg`, `.png`, or `.jpg`).

## Workflow
1. Generate artifacts with `scripts/generate_favicons_playwright.py`.
2. Apply snippet and manifest merge with `scripts/apply_favicon_refs.py`.
3. Validate the updated files in `public/`, `index.html`, and `site.webmanifest`.

## Commands
Generate files from an icon:
```bash
python3 scripts/generate_favicons_playwright.py \
  --source /absolute/path/to/favicon.svg \
  --project-root /absolute/path/to/project
```

Apply references to `index.html` and merge manifest:
```bash
python3 scripts/apply_favicon_refs.py \
  --project-root /absolute/path/to/project
```

Optional headed run for debugging:
```bash
python3 scripts/generate_favicons_playwright.py \
  --source /absolute/path/to/favicon.svg \
  --project-root /absolute/path/to/project \
  --headed
```

Keep Playwright temp files for debugging (default is auto-cleanup):
```bash
python3 scripts/generate_favicons_playwright.py \
  --source /absolute/path/to/favicon.svg \
  --project-root /absolute/path/to/project \
  --keep-temp
```

## Outputs
Generation script writes to the target `public/` directory:
- Favicon artifacts from RFG zip (`favicon.ico`, `favicon.svg`, PNG icons).
- `favicon-instructions.rfg.html` (captured `<head>` snippet from RFG result page).
- `site.webmanifest.rfg.generated.json` (generated manifest candidate for merge).
- Removes `project/.playwright-cli` automatically after execution unless `--keep-temp` is set.

Apply script updates:
- `index.html` using marker block:
  - `<!-- rfg-favicon:start -->`
  - `<!-- rfg-favicon:end -->`
- `public/site.webmanifest` with conservative merge:
  - Always refresh `icons` from generated manifest.
  - Preserve existing app metadata by default.

## Decision Rules
- Prefer this skill when user explicitly wants RealFaviconGenerator output.
- Prefer non-destructive updates; replace only marker block in `index.html`.
- Prefer merge over overwrite for existing `site.webmanifest`.
- Re-run generation when source icon or favicon path requirements change.

## Troubleshooting
- If upload fails through CLI `upload`, rely on `setInputFiles` path implemented in the script.
- If RFG UI changes and button labels differ, update selectors in `generate_favicons_playwright.py`.
- If `PWCLI` cannot be found, set `--pwcli` explicitly.

## References
- Playwright flow details: `references/rfg-flow.md`
