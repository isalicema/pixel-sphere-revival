#!/usr/bin/env python3
"""Render the enlarged Photo Sphere glyph with a multicolor gradient and shadow."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


EXPECTED_SOURCE_SHA256 = "a0bf96ec92437c4aec8e7c97bb9741fc08ca319cafac3ab037131e944e997b94"
CANVAS_SIZE = 432
GLYPH_SIZE = 272
BACKGROUND = (21, 21, 21, 255)
COLOR_STOPS = (
    (0.00, (255, 75, 62)),   # coral red
    (0.24, (255, 159, 28)),  # amber
    (0.48, (255, 61, 141)),  # magenta
    (0.72, (168, 85, 247)),  # violet
    (1.00, (59, 130, 246)),  # cobalt blue
)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def color_at(position: float) -> tuple[int, int, int]:
    for index in range(len(COLOR_STOPS) - 1):
        left_position, left_color = COLOR_STOPS[index]
        right_position, right_color = COLOR_STOPS[index + 1]
        if position <= right_position:
            span = right_position - left_position
            amount = 0 if span == 0 else (position - left_position) / span
            return tuple(round(left + (right - left) * amount) for left, right in zip(left_color, right_color))
    return COLOR_STOPS[-1][1]


if len(sys.argv) != 2:
    raise SystemExit(f"usage: {Path(sys.argv[0]).name} /path/to/quantum_ic_panorama_photosphere_white_24.png")

source_path = Path(sys.argv[1]).resolve()
if not source_path.is_file():
    raise SystemExit(f"source icon not found: {source_path}")
if sha256(source_path) != EXPECTED_SOURCE_SHA256:
    raise SystemExit(f"unexpected source icon: {source_path}")

project_root = Path(__file__).resolve().parents[1]
foreground_path = project_root / "assets/icon/photosphere-icon-native-gradient-v3-foreground.png"
launcher_path = project_root / "assets/icon/photosphere-icon-native-gradient-v3-launcher.png"
preview_path = project_root / "assets/icon/photosphere-icon-native-gradient-v3-preview.png"

glyph_alpha = Image.open(source_path).convert("RGBA").resize(
    (GLYPH_SIZE, GLYPH_SIZE), Image.Resampling.LANCZOS
).getchannel("A")

gradient = Image.new("RGBA", (GLYPH_SIZE, GLYPH_SIZE), (0, 0, 0, 0))
pixels = gradient.load()
for y in range(GLYPH_SIZE):
    for x in range(GLYPH_SIZE):
        position = (0.72 * x + 0.28 * y) / (GLYPH_SIZE - 1)
        red, green, blue = color_at(position)
        pixels[x, y] = (red, green, blue, glyph_alpha.getpixel((x, y)))

offset = ((CANVAS_SIZE - GLYPH_SIZE) // 2,) * 2
shadow_alpha = glyph_alpha.filter(ImageFilter.GaussianBlur(14))
shadow_alpha = shadow_alpha.point(lambda value: round(value * 0.72))
shadow = Image.new("RGBA", (GLYPH_SIZE, GLYPH_SIZE), (0, 0, 0, 0))
shadow.putalpha(shadow_alpha)

foreground = Image.new("RGBA", (CANVAS_SIZE, CANVAS_SIZE), (0, 0, 0, 0))
foreground.alpha_composite(shadow, (offset[0], offset[1] + 12))
foreground.alpha_composite(gradient, offset)
foreground.save(foreground_path)

launcher = Image.new("RGBA", (CANVAS_SIZE, CANVAS_SIZE), BACKGROUND)
launcher.alpha_composite(foreground)
launcher.save(launcher_path)

preview = Image.new("RGB", (640, 480), (230, 230, 230))
preview_icon = launcher.resize((144, 144), Image.Resampling.LANCZOS)
preview_mask = Image.new("L", (144, 144), 0)
ImageDraw.Draw(preview_mask).rounded_rectangle((0, 0, 143, 143), radius=34, fill=255)
preview.paste(preview_icon, ((preview.width - 144) // 2, (preview.height - 144) // 2), preview_mask)
preview.save(preview_path)

for output in (foreground_path, launcher_path, preview_path):
    print(output)
