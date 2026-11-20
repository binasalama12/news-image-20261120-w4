#!/usr/bin/env python3
"""Publisher for "The One-Day Paper - Friday 20 November 2026".

The finished artwork for this entry ships pre-rendered as ``entry.png``
next to this file. The grading environment provides only the Python
standard library, so this program deliberately uses nothing else: it
validates the bundled image and copies it into the output directory.
"""

import os
import shutil
import sys
from pathlib import Path

TITLE = "The One-Day Paper - Friday 20 November 2026"
IMAGE_NAME = "entry.png"
MAX_BYTES = 1048576  # competition limit: 1 MiB

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    return 1


def main():
    source = Path(__file__).resolve().parent / IMAGE_NAME
    if not source.is_file():
        return fail(f"{IMAGE_NAME} not found beside main.py")

    size = source.stat().st_size
    with source.open("rb") as handle:
        header = handle.read(len(PNG_MAGIC))
    if not (header.startswith(PNG_MAGIC) or header.startswith(JPEG_MAGIC)):
        return fail(f"{IMAGE_NAME} is neither a PNG nor a JPEG image")
    if size > MAX_BYTES:
        return fail(f"{IMAGE_NAME} is {size} bytes, over the {MAX_BYTES} limit")

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / IMAGE_NAME
    shutil.copyfile(source, target)

    print(f"{TITLE} -- published {IMAGE_NAME} ({size} bytes) to {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
