#!/usr/bin/env python3
"""Apply RealFaviconGenerator head snippet and merge web manifest safely."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

START_MARKER = "<!-- rfg-favicon:start -->"
END_MARKER = "<!-- rfg-favicon:end -->"
LEGACY_TAG_PATTERNS = [
    r'<link[^>]*rel="icon"[^>]*>',
    r'<link[^>]*rel="shortcut icon"[^>]*>',
    r'<link[^>]*rel="apple-touch-icon"[^>]*>',
    r'<link[^>]*rel="manifest"[^>]*>',
]


def normalize_snippet(raw: str) -> str:
    # RFG often returns the snippet as a single line. Keep one tag per line for readability.
    pieces = [part.strip() for part in re.split(r"(?=<link )", raw) if part.strip()]
    if not pieces:
        return raw.strip()
    return "\n".join(pieces)


def render_block(snippet: str) -> str:
    normalized = normalize_snippet(snippet)
    lines = [START_MARKER]
    lines.extend(normalized.splitlines())
    lines.append(END_MARKER)
    return "\n".join(lines)


def upsert_favicon_block(index_html_path: Path, block: str) -> bool:
    content = index_html_path.read_text(encoding="utf-8")

    if START_MARKER in content and END_MARKER in content:
        pattern = re.compile(
            re.escape(START_MARKER) + r".*?" + re.escape(END_MARKER),
            flags=re.DOTALL,
        )
        new_content = pattern.sub(block, content, count=1)
    else:
        for pattern in LEGACY_TAG_PATTERNS:
            content = re.sub(rf"[ \t]*{pattern}[ \t]*\n?", "", content, flags=re.IGNORECASE)

        head_close = "</head>"
        pos = content.lower().find(head_close)
        if pos == -1:
            raise RuntimeError(f"Could not find </head> in {index_html_path}")

        insertion = "\n  " + block.replace("\n", "\n  ") + "\n"
        new_content = content[:pos] + insertion + content[pos:]

    changed = new_content != content
    if changed:
        index_html_path.write_text(new_content, encoding="utf-8")
    return changed


def merge_manifest(existing_path: Path, generated_path: Path) -> bool:
    generated = json.loads(generated_path.read_text(encoding="utf-8"))

    if existing_path.exists():
        existing = json.loads(existing_path.read_text(encoding="utf-8"))
    else:
        existing = {}

    merged = dict(existing)

    # Preserve project-specific identity fields by default, but always refresh icon-related data.
    for key in [
        "id",
        "start_url",
        "scope",
        "display",
        "name",
        "short_name",
        "theme_color",
        "background_color",
    ]:
        if key not in merged and key in generated:
            merged[key] = generated[key]

    if "icons" in generated:
        merged["icons"] = generated["icons"]

    if "screenshots" in generated and "screenshots" not in merged:
        merged["screenshots"] = generated["screenshots"]

    changed = merged != existing
    if changed:
        existing_path.write_text(json.dumps(merged, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    return changed


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Apply favicon refs to index.html and merge site.webmanifest"
    )
    parser.add_argument("--project-root", required=True, help="Project root")
    parser.add_argument(
        "--public-dir",
        default="public",
        help="Public directory relative to project root (default: public)",
    )
    parser.add_argument(
        "--index-html",
        default="index.html",
        help="Index HTML file relative to project root (default: index.html)",
    )
    parser.add_argument(
        "--snippet-file",
        default="favicon-instructions.rfg.html",
        help="Snippet file relative to public dir (default: favicon-instructions.rfg.html)",
    )
    parser.add_argument(
        "--generated-manifest",
        default="site.webmanifest.rfg.generated.json",
        help="Generated manifest filename relative to public dir",
    )
    args = parser.parse_args()

    project_root = Path(args.project_root).expanduser().resolve()
    public_dir = project_root / args.public_dir
    index_html = project_root / args.index_html

    if not project_root.exists():
        raise FileNotFoundError(f"Project root not found: {project_root}")
    if not index_html.exists():
        raise FileNotFoundError(f"index.html not found: {index_html}")

    snippet_path = public_dir / args.snippet_file
    if not snippet_path.exists():
        raise FileNotFoundError(f"Snippet file not found: {snippet_path}")

    snippet = snippet_path.read_text(encoding="utf-8").strip()
    if not snippet:
        raise RuntimeError(f"Snippet file is empty: {snippet_path}")

    block = render_block(snippet)
    html_changed = upsert_favicon_block(index_html, block)

    generated_manifest_path = public_dir / args.generated_manifest
    manifest_path = public_dir / "site.webmanifest"
    manifest_changed = False
    if generated_manifest_path.exists():
        manifest_changed = merge_manifest(manifest_path, generated_manifest_path)

    print("[OK] Applied favicon references")
    print(f"- index.html updated: {html_changed}")
    print(f"- site.webmanifest updated: {manifest_changed}")
    print(f"- marker block: {START_MARKER} ... {END_MARKER}")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"[ERROR] {exc}")
        sys.exit(1)
