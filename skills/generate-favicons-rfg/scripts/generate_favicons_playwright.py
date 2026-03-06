#!/usr/bin/env python3
"""Generate favicon artifacts from realfavicongenerator.net using Playwright CLI.

This script automates the browser flow, downloads favicon.zip, extracts assets to
project public dir, and stores the generated head snippet for idempotent integration.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from zipfile import ZipFile

RFG_URL = "https://realfavicongenerator.net/"
DEFAULT_HEAD_SNIPPET = """<link rel="icon" type="image/png" href="/favicon-96x96.png" sizes="96x96" />
<link rel="icon" type="image/svg+xml" href="/favicon.svg" />
<link rel="shortcut icon" href="/favicon.ico" />
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png" />
<link rel="manifest" href="/site.webmanifest" />"""


def run_cmd(cmd: list[str], env: dict[str, str], cwd: Path | None = None) -> str:
    proc = subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(f"Command failed ({' '.join(cmd)}):\n{proc.stdout}")
    if "### Error" in proc.stdout:
        raise RuntimeError(f"Command reported Playwright error ({' '.join(cmd)}):\n{proc.stdout}")
    return proc.stdout


def extract_result_value(output: str) -> str:
    marker = "### Result"
    idx = output.find(marker)
    if idx == -1:
        raise RuntimeError(f"Could not parse run-code result from output:\n{output}")

    tail = output[idx + len(marker) :].lstrip("\n")
    first_line = tail.splitlines()[0].strip()
    if not first_line:
        raise RuntimeError(f"Empty run-code result. Output:\n{output}")

    try:
        parsed = json.loads(first_line)
    except json.JSONDecodeError:
        parsed = first_line

    if isinstance(parsed, str):
        return parsed
    return json.dumps(parsed)


def resolve_pwcli(args: argparse.Namespace) -> Path:
    if args.pwcli:
        path = Path(args.pwcli).expanduser().resolve()
    elif os.environ.get("PWCLI"):
        path = Path(os.environ["PWCLI"]).expanduser().resolve()
    else:
        codex_home = Path(os.environ.get("CODEX_HOME", Path.home() / ".codex"))
        path = codex_home / "skills/playwright/scripts/playwright_cli.sh"

    if not path.exists():
        raise FileNotFoundError(
            f"Playwright wrapper not found at {path}. Set --pwcli or PWCLI env var."
        )
    if not os.access(path, os.X_OK):
        raise PermissionError(f"Playwright wrapper is not executable: {path}")
    return path


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def prepare_upload_source(source: Path, project_root: Path, work_dir: Path) -> Path:
    """Ensure uploaded file is inside project root (Playwright CLI allowed roots)."""
    try:
        source.relative_to(project_root)
        return source
    except ValueError:
        pass

    safe_name = f"source-icon{source.suffix.lower() or '.svg'}"
    local_source = work_dir / safe_name
    shutil.copy2(source, local_source)
    return local_source


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate favicons via RealFaviconGenerator using Playwright CLI"
    )
    parser.add_argument("--source", required=True, help="Path to source icon (svg/png/jpg)")
    parser.add_argument("--project-root", required=True, help="Target project root")
    parser.add_argument(
        "--public-dir",
        default="public",
        help="Public directory relative to project root (default: public)",
    )
    parser.add_argument(
        "--session",
        default="rfg",
        help="Playwright CLI session name (default: rfg)",
    )
    parser.add_argument("--pwcli", help="Path to playwright_cli.sh wrapper")
    parser.add_argument(
        "--headed",
        action="store_true",
        help="Run browser with UI",
    )
    parser.add_argument(
        "--keep-zip",
        action="store_true",
        help="Keep downloaded favicon.zip in public dir",
    )
    parser.add_argument(
        "--keep-temp",
        action="store_true",
        help="Keep .playwright-cli temporary artifacts",
    )

    args = parser.parse_args()

    source = Path(args.source).expanduser().resolve()
    if not source.exists():
        raise FileNotFoundError(f"Source icon not found: {source}")

    project_root = Path(args.project_root).expanduser().resolve()
    if not project_root.exists():
        raise FileNotFoundError(f"Project root not found: {project_root}")

    public_dir = project_root / args.public_dir
    public_dir.mkdir(parents=True, exist_ok=True)

    pwcli = resolve_pwcli(args)

    env = os.environ.copy()
    env["PLAYWRIGHT_CLI_SESSION"] = args.session

    # Keep playwright artifact output inside the target project to avoid cross-project leaks.
    pw_artifacts_dir = project_root / ".playwright-cli"
    pw_artifacts_dir.mkdir(parents=True, exist_ok=True)
    upload_work_dir = pw_artifacts_dir / "upload"
    upload_work_dir.mkdir(parents=True, exist_ok=True)
    upload_source = prepare_upload_source(source, project_root, upload_work_dir)

    open_cmd = [str(pwcli), "open", RFG_URL]
    if args.headed:
        open_cmd.append("--headed")

    print("[1/6] Opening RealFaviconGenerator...")
    run_cmd(open_cmd, env, cwd=project_root)

    try:
        print("[2/6] Uploading source icon...")
        run_cmd(
            [
                str(pwcli),
                "run-code",
                (
                    "async (page) => { "
                    f"await page.setInputFiles('input[type=file]', {json.dumps(str(upload_source))}); "
                    "return 'uploaded'; "
                    "}"
                ),
            ],
            env,
            cwd=project_root,
        )

        print("[3/6] Advancing to the result page...")
        run_cmd(
            [
                str(pwcli),
                "run-code",
                (
                    "async (page) => { "
                    "await page.getByRole('button', { name: /^Next$/i }).click(); "
                    "await page.waitForURL('**/your-favicon-is-ready', { timeout: 60000 }); "
                    "return page.url(); "
                    "}"
                ),
            ],
            env,
            cwd=project_root,
        )

        print("[4/6] Capturing HTML head snippet from instructions...")
        snippet = None
        for attempt in range(1, 13):
            try:
                snippet_output = run_cmd(
                    [
                        str(pwcli),
                        "run-code",
                        (
                            "async (page) => { "
                            "const blocks = await page.locator('code').allInnerTexts(); "
                            "const snippet = blocks.find((txt) => txt.includes('<link rel=')); "
                            "if (!snippet) throw new Error('Could not find HTML snippet block on page'); "
                            "return snippet; "
                            "}"
                        ),
                    ],
                    env,
                    cwd=project_root,
                )
                snippet = extract_result_value(snippet_output)
                break
            except Exception:
                if attempt == 12:
                    snippet = DEFAULT_HEAD_SNIPPET
                    print(
                        "[WARN] Could not capture snippet from page after retries; using default snippet."
                    )
                    break
                time.sleep(1.0)

        if snippet is None:
            snippet = DEFAULT_HEAD_SNIPPET

        zip_path = pw_artifacts_dir / "favicon.zip"
        if zip_path.exists():
            zip_path.unlink()

        print("[5/6] Downloading favicon package...")
        download_ok = False
        for attempt in range(1, 13):
            try:
                run_cmd(
                    [
                        str(pwcli),
                        "run-code",
                        (
                            "async (page) => { "
                            "const downloadButton = page.getByRole('button', { name: /^Download$/i }).first(); "
                            "const [download] = await Promise.all(["
                            "page.waitForEvent('download', { timeout: 60000 }),"
                            "downloadButton.click({ force: true })"
                            "]); "
                            f"await download.saveAs({json.dumps(str(zip_path))}); "
                            "return download.suggestedFilename(); "
                            "}"
                        ),
                    ],
                    env,
                    cwd=project_root,
                )
                download_ok = True
                break
            except Exception:
                if attempt == 12:
                    raise
                time.sleep(1.0)

        if not download_ok:
            raise RuntimeError("Failed to download favicon.zip from RFG")

        if not zip_path.exists():
            raise FileNotFoundError(f"Expected downloaded zip not found: {zip_path}")

        print("[6/6] Extracting files into public directory...")
        generated_manifest = public_dir / "site.webmanifest.rfg.generated.json"
        with tempfile.TemporaryDirectory(prefix="rfg-extract-") as tmp_dir_raw:
            tmp_dir = Path(tmp_dir_raw)
            with ZipFile(zip_path) as zf:
                zf.extractall(tmp_dir)

            for file_path in tmp_dir.iterdir():
                if not file_path.is_file():
                    continue
                if file_path.name == "site.webmanifest":
                    shutil.copy2(file_path, generated_manifest)
                else:
                    shutil.copy2(file_path, public_dir / file_path.name)

        snippet_file = public_dir / "favicon-instructions.rfg.html"
        write_file(snippet_file, snippet + "\n")

        if args.keep_zip:
            shutil.copy2(zip_path, public_dir / "favicon.zip")

        print("\n[OK] Favicon artifacts generated successfully")
        print(f"- Public dir: {public_dir}")
        print(f"- Snippet file: {snippet_file}")
        print(f"- Generated manifest candidate: {generated_manifest}")
        return 0
    finally:
        # Always close browser session to avoid stale state in subsequent runs.
        try:
            run_cmd([str(pwcli), "close"], env, cwd=project_root)
        except Exception:
            pass
        if not args.keep_temp:
            shutil.rmtree(pw_artifacts_dir, ignore_errors=True)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:
        print(f"[ERROR] {exc}")
        sys.exit(1)
