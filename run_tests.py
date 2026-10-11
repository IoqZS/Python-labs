from pathlib import Path
import subprocess
import sys


if __name__ == "__main__":
    root = Path(__file__).parent
    for number in range(6, 12):
        print(f"\nЛабораторная {number}", flush=True)
        result = subprocess.run([sys.executable, "-m", "pytest", "-q"], cwd=root / f"Практика {number}")
        if result.returncode:
            sys.exit(result.returncode)
