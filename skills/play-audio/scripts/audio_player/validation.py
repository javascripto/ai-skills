import sys
from pathlib import Path


class AudioPathError(RuntimeError):
    pass


def resolve_audio_path(raw_path: str) -> Path:
    audio_path = Path(raw_path).expanduser().resolve()
    if not audio_path.exists():
        print(f"Audio file not found: {audio_path}", file=sys.stderr)
        raise AudioPathError("Unable to play the requested audio file.")
    if not audio_path.is_file():
        print(f"Path is not a file: {audio_path}", file=sys.stderr)
        raise AudioPathError("Unable to play the requested audio file.")
    return audio_path
