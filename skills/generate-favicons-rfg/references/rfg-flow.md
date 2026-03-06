# RealFaviconGenerator Playwright Flow

## Purpose
Use this reference when automating the site flow with Playwright.

## Verified flow
1. Open `https://realfavicongenerator.net/`.
2. Upload source icon to `input[type=file]` using `page.setInputFiles(...)`.
3. Click `Next` and wait for URL `**/your-favicon-is-ready`.
4. Read HTML snippet from the result page (`code` block containing `<link rel="icon" ...>`).
5. Click `Download` and wait for download event (`favicon.zip`).
6. Extract artifacts and integrate into project `public/`.

## Why `setInputFiles`
The Playwright CLI `upload` command depends on a modal-state helper. On this site, direct DOM upload via `setInputFiles` is the stable path.

## Expected generated files
- `favicon.svg`
- `favicon-96x96.png`
- `favicon.ico`
- `apple-touch-icon.png`
- `web-app-manifest-192x192.png`
- `web-app-manifest-512x512.png`
- `site.webmanifest`

## Integration policy
- Update `index.html` via marker block replacement, never full overwrite.
- Merge `site.webmanifest` conservatively: always refresh `icons`, preserve existing app metadata by default.
