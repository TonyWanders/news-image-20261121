#!/usr/bin/env python3
# Entry for "Sum up 21 November's world news in one image".
# The entry is the finished picture in this folder, entry.png.
# This script only places that picture where the judge expects it:
# /output/entry.png (or a path given on the command line).
# It never touches the network, never uses the clock, and never
# invents bytes, so every run writes exactly the same file.
import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).parent
PICTURE = HERE / "entry.png"


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        while True:
            block = f.read(1 << 16)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def run(target):
    target.parent.mkdir(parents=True, exist_ok=True)
    if not PICTURE.exists():
        print("entry.png is missing from this folder", file=sys.stderr)
        return 1
    data = PICTURE.read_bytes()
    target.write_bytes(data)
    if digest(target) != digest(PICTURE):
        print("copy failed: output does not match entry.png", file=sys.stderr)
        return 1
    print(f"wrote {target} ({len(data)} bytes)")
    return 0


if __name__ == "__main__":
    import os

    out = sys.argv[1] if len(sys.argv) > 1 else os.environ.get("OUTPUT_PATH", "/output/entry.png")
    raise SystemExit(run(Path(out)))
