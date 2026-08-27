#!/usr/bin/env python3
"""Report compression and mmap alignment of native libraries inside an APK."""

from __future__ import annotations

import argparse
import json
import struct
import zipfile
from pathlib import Path


LOCAL_FILE_HEADER = b"PK\x03\x04"


def entry_data_offset(apk: Path, header_offset: int) -> int:
    with apk.open("rb") as stream:
        stream.seek(header_offset)
        header = stream.read(30)
    if len(header) != 30 or header[:4] != LOCAL_FILE_HEADER:
        raise ValueError(f"invalid local ZIP header at byte {header_offset}")
    filename_length, extra_length = struct.unpack_from("<HH", header, 26)
    return header_offset + 30 + filename_length + extra_length


def inspect(apk: Path) -> dict[str, object]:
    libraries: list[dict[str, object]] = []
    with zipfile.ZipFile(apk) as archive:
        for info in sorted(archive.infolist(), key=lambda item: item.filename):
            if not (info.filename.startswith("lib/") and info.filename.endswith(".so")):
                continue
            data_offset = entry_data_offset(apk, info.header_offset)
            libraries.append(
                {
                    "path": info.filename,
                    "compression": "stored" if info.compress_type == zipfile.ZIP_STORED else f"method-{info.compress_type}",
                    "size_bytes": info.file_size,
                    "data_offset": data_offset,
                    "aligned_4096": data_offset % 4096 == 0,
                    "aligned_16384": data_offset % 16384 == 0,
                }
            )
    return {
        "apk": str(apk.resolve()),
        "native_library_count": len(libraries),
        "all_stored": all(item["compression"] == "stored" for item in libraries),
        "all_aligned_4096": all(item["aligned_4096"] for item in libraries),
        "all_aligned_16384": all(item["aligned_16384"] for item in libraries),
        "libraries": libraries,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("apk", type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.apk), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
