import shutil
from pathlib import Path

from .process import run_command


def play_macos(audio_path: Path) -> int:
    if shutil.which("afplay"):
        return run_command("afplay", ["afplay", str(audio_path)])
    raise RuntimeError("afplay is not available on this macOS system.")


def play_linux(audio_path: Path) -> int:
    candidates = [
        ("pw-play", ["pw-play", str(audio_path)]),
        ("paplay", ["paplay", str(audio_path)]),
        ("aplay", ["aplay", str(audio_path)]),
        ("ffplay", ["ffplay", "-nodisp", "-autoexit", "-loglevel", "error", str(audio_path)]),
    ]
    for label, cmd in candidates:
        if shutil.which(cmd[0]):
            return run_command(label, cmd)
    raise RuntimeError("No supported Linux audio backend found (tried pw-play, paplay, aplay, ffplay).")


def play_windows(audio_path: Path) -> int:
    powershell = shutil.which("powershell") or shutil.which("powershell.exe") or shutil.which("pwsh")
    if not powershell:
        raise RuntimeError("PowerShell is not available on this Windows system.")

    ps_script = (
        "Add-Type -AssemblyName PresentationCore; "
        "$path = [System.IO.Path]::GetFullPath($args[0]); "
        "$player = New-Object System.Windows.Media.MediaPlayer; "
        "$player.Open([System.Uri]::new($path)); "
        "$player.Volume = 1.0; "
        "$player.Play(); "
        "while (-not $player.NaturalDuration.HasTimeSpan) { Start-Sleep -Milliseconds 100 }; "
        "Start-Sleep -Milliseconds ([int][Math]::Ceiling($player.NaturalDuration.TimeSpan.TotalMilliseconds)); "
        "$player.Stop(); "
        "$player.Close();"
    )
    return run_command(
        "powershell-mediaplayer",
        [powershell, "-NoProfile", "-Command", ps_script, str(audio_path)],
    )

