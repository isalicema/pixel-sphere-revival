#!/usr/bin/env python3
"""Package the base APK's built-in Photo Sphere glyph as launcher resources."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

from PIL import Image, ImageDraw


EXPECTED_SOURCE_SHA256 = "a0bf96ec92437c4aec8e7c97bb9741fc08ca319cafac3ab037131e944e997b94"
CANVAS_SIZE = 432
GLYPH_SIZE = 216
BACKGROUND = (21, 21, 21, 255)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


if len(sys.argv) != 2:
    raise SystemExit(f"usage: {Path(sys.argv[0]).name} /path/to/quantum_ic_panorama_photosphere_white_24.png")

source_path = Path(sys.argv[1]).resolve()
if not source_path.is_file():
    raise SystemExit(f"source icon not found: {source_path}")
if sha256(source_path) != EXPECTED_SOURCE_SHA256:
    raise SystemExit(f"unexpected source icon: {source_path}")

project_root = Path(__file__).resolve().parents[1]
foreground_path = project_root / "assets/android/res/drawable-nodpi/photosphere_icon_foreground.png"
launcher_path = project_root / "assets/android/res/mipmap-nodpi/photosphere_launcher.png"
preview_path = project_root / "assets/icon/photosphere-icon-native-preview.png"

glyph = Image.open(source_path).convert("RGBA").resize(
    (GLYPH_SIZE, GLYPH_SIZE), Image.Resampling.LANCZOS
)
offset = ((CANVAS_SIZE - GLYPH_SIZE) // 2,) * 2

foreground = Image.new("RGBA", (CANVAS_SIZE, CANVAS_SIZE), (0, 0, 0, 0))
foreground.alpha_composite(glyph, offset)
foreground.save(foreground_path)

launcher = Image.new("RGBA", (CANVAS_SIZE, CANVAS_SIZE), (0, 0, 0, 0))
launcher_background = Image.new("RGBA", (CANVAS_SIZE, CANVAS_SIZE), BACKGROUND)
launcher.alpha_composite(launcher_background)
launcher.alpha_composite(glyph, offset)
launcher.save(launcher_path)

preview = Image.new("RGB", (640, 480), (230, 230, 230))
preview_icon = launcher.resize((144, 144), Image.Resampling.LANCZOS)
preview_mask = Image.new("L", (144, 144), 0)
ImageDraw.Draw(preview_mask).rounded_rectangle((0, 0, 143, 143), radius=34, fill=255)
preview.paste(preview_icon, ((preview.width - 144) // 2, (preview.height - 144) // 2), preview_mask)
preview.save(preview_path)

for output in (foreground_path, launcher_path, preview_path):
    print(output)
