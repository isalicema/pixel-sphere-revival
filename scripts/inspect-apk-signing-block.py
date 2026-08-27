#!/usr/bin/env python3
"""Inspect APK Signing Block scheme IDs without modifying the APK."""

from __future__ import annotations

import argparse
import json
import struct
from pathlib import Path


EOCD_MAGIC = b"PK\x05\x06"
APK_SIG_MAGIC = b"APK Sig Block 42"
SCHEME_IDS = {
    0x7109871A: "APK Signature Scheme v2",
    0xF05368C0: "APK Signature Scheme v3",
    0x1B93AD61: "APK Signature Scheme v3.1",
    0x2B09189E: "APK Signature Scheme v4 (legacy/provisional ID)",
    0x6DFF800D: "Source stamp",
    0x42726577: "Verity padding",
}


def find_eocd(data: bytes) -> int:
    # ZIP comments are limited to 65,535 bytes, so the EOCD must be near EOF.
    search_start = max(0, len(data) - 22 - 65535)
    offset = data.rfind(EOCD_MAGIC, search_start)
    if offset < 0:
        raise ValueError("ZIP end-of-central-directory record not found")
    if offset + 22 > len(data):
        raise ValueError("truncated ZIP end-of-central-directory record")
    comment_length = struct.unpack_from("<H", data, offset + 20)[0]
    if offset + 22 + comment_length != len(data):
        raise ValueError("ambiguous ZIP end-of-central-directory record")
    return offset


def inspect(path: Path) -> dict[str, object]:
    data = path.read_bytes()
    eocd_offset = find_eocd(data)
    central_directory_offset = struct.unpack_from("<I", data, eocd_offset + 16)[0]

    result: dict[str, object] = {
        "path": str(path.resolve()),
        "size_bytes": len(data),
        "zip_eocd_offset": eocd_offset,
        "central_directory_offset": central_directory_offset,
        "apk_signing_block_present": False,
        "schemes": [],
        "pairs": [],
    }

    footer_offset = central_directory_offset - 24
    if footer_offset < 0 or data[footer_offset + 8 : central_directory_offset] != APK_SIG_MAGIC:
        return result

    footer_size = struct.unpack_from("<Q", data, footer_offset)[0]
    block_offset = central_directory_offset - footer_size - 8
    if block_offset < 0:
        raise ValueError("invalid APK Signing Block size")
    header_size = struct.unpack_from("<Q", data, block_offset)[0]
    if header_size != footer_size:
        raise ValueError("APK Signing Block header/footer sizes differ")

    pairs: list[dict[str, object]] = []
    schemes: list[str] = []
    cursor = block_offset + 8
    while cursor < footer_offset:
        if cursor + 8 > footer_offset:
            raise ValueError("truncated APK Signing Block pair length")
        pair_length = struct.unpack_from("<Q", data, cursor)[0]
        cursor += 8
        if pair_length < 4 or cursor + pair_length > footer_offset:
            raise ValueError("invalid APK Signing Block pair length")
        pair_id = struct.unpack_from("<I", data, cursor)[0]
        value_length = pair_length - 4
        name = SCHEME_IDS.get(pair_id, "unknown")
        pairs.append(
            {
                "id_hex": f"0x{pair_id:08x}",
                "name": name,
                "value_size_bytes": value_length,
            }
        )
        if name.startswith("APK Signature Scheme"):
            schemes.append(name)
        cursor += pair_length

    if cursor != footer_offset:
        raise ValueError("APK Signing Block pair table does not end at footer")

    result.update(
        {
            "apk_signing_block_present": True,
            "apk_signing_block_offset": block_offset,
            "apk_signing_block_size_bytes": footer_size + 8,
            "schemes": schemes,
            "pairs": pairs,
        }
    )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("apk", type=Path)
    args = parser.parse_args()
    print(json.dumps(inspect(args.apk), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
