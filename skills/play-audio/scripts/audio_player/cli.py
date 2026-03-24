import argparse
import platform
import sys

from .backends import play_linux, play_macos, play_windows
from .validation import AudioPathError, resolve_audio_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Play a local audio file on macOS, Linux, or Windows.")
    parser.add_argument("audio_file", help="Path to the local audio file to reproduce")
    args = parser.parse_args()

    try:
        audio_path = resolve_audio_path(args.audio_file)
        system = platform.system()
        if system == "Darwin":
            return play_macos(audio_path)
        if system == "Linux":
            return play_linux(audio_path)
        if system == "Windows":
            return play_windows(audio_path)
        raise RuntimeError(f"Unsupported platform: {system}")
    except AudioPathError:
        return 1
    except RuntimeError as exc:
        print(str(exc), file=sys.stderr)
        return 2
