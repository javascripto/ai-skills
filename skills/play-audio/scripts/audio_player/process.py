import subprocess


def run_command(label: str, cmd: list[str]) -> int:
    print(f"Playing via {label}: {' '.join(cmd[1:] if len(cmd) > 1 else cmd)}")
    completed = subprocess.run(cmd, check=False)
    return completed.returncode

