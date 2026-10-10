#!/usr/bin/env python3
"""Render Alice-approved blue-wrap v6 artwork as Android launcher resources."""

from __future__ import annotations

import hashlib
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw


EXPECTED_ARTWORK_SHA256 = "c1a911c74c19e7a77fabd3f6955ae1226d6f57fa35c3793090203e192192bc3c"
EXPECTED_MONOCHROME_SHA256 = "7a6c0c1d63a36be797db8a8e98007be813b1713887149a89ab480ec937cf34b2"
CANVAS_SIZE = 432
BADGE_BOUNDS = (42, 42, 390, 390)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify(path: Path, expected: str) -> None:
    if not path.is_file():
        raise SystemExit(f"required source not found: {path}")
    actual = sha256(path)
    if actual != expected:
        raise SystemExit(f"unexpected source hash for {path}: {actual}")


project_root = Path(__file__).resolve().parents[1]
artwork_path = project_root / "assets/icon/photosphere-icon-native-blue-wrap-v6.png"
monochrome_source_path = project_root / "assets/icon/photosphere-icon-monochrome-source.png"
foreground_path = project_root / "assets/android/res/drawable-nodpi/photosphere_icon_foreground.png"
monochrome_path = project_root / "assets/android/res/drawable-nodpi/photosphere_icon_monochrome_mask.png"
launcher_path = project_root / "assets/android/res/mipmap-nodpi/photosphere_launcher.png"
preview_path = project_root / "assets/icon/photosphere-icon-approved-v6-android-preview.png"

verify(artwork_path, EXPECTED_ARTWORK_SHA256)
verify(monochrome_source_path, EXPECTED_MONOCHROME_SHA256)

artwork = Image.open(artwork_path).convert("RGBA").resize(
    (CANVAS_SIZE, CANVAS_SIZE), Image.Resampling.LANCZOS
)

# Image generation left a few isolated semi-transparent pixels outside the badge.
# Clip to a supersampled circle while retaining the artwork's internal alpha.
mask_scale = 4
circle_mask = Image.new("L", (CANVAS_SIZE * mask_scale,) * 2, 0)
scaled_bounds = tuple(value * mask_scale for value in BADGE_BOUNDS)
ImageDraw.Draw(circle_mask).ellipse(scaled_bounds, fill=255)
circle_mask = circle_mask.resize((CANVAS_SIZE, CANVAS_SIZE), Image.Resampling.LANCZOS)
artwork.putalpha(ImageChops.multiply(artwork.getchannel("A"), circle_mask))

foreground_path.parent.mkdir(parents=True, exist_ok=True)
launcher_path.parent.mkdir(parents=True, exist_ok=True)
artwork.save(foreground_path)
artwork.save(launcher_path)

monochrome = Image.open(monochrome_source_path).convert("RGBA")
if monochrome.size != (CANVAS_SIZE, CANVAS_SIZE):
    raise SystemExit(f"unexpected monochrome source size: {monochrome.size}")
monochrome.save(monochrome_path)

preview = Image.new("RGBA", (640, 480), (235, 235, 235, 255))
preview_icon = artwork.resize((144, 144), Image.Resampling.LANCZOS)
preview.alpha_composite(preview_icon, ((preview.width - 144) // 2, (preview.height - 144) // 2))
preview.convert("RGB").save(preview_path)

for output in (foreground_path, monochrome_path, launcher_path, preview_path):
    print(f"{output}: {sha256(output)}")
