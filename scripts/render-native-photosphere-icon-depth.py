#!/usr/bin/env python3
"""Render a larger Photo Sphere glyph with subtle depth and folded end caps."""

from __future__ import annotations

import hashlib
import sys
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFilter


EXPECTED_SOURCE_SHA256 = "a0bf96ec92437c4aec8e7c97bb9741fc08ca319cafac3ab037131e944e997b94"
CANVAS_SIZE = 432
GLYPH_SIZE = 272
BACKGROUND = (21, 21, 21, 255)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def scaled_polygon(points: list[tuple[float, float]]) -> list[tuple[int, int]]:
    scale = GLYPH_SIZE / 96
    return [(round(x * scale), round(y * scale)) for x, y in points]


if len(sys.argv) != 2:
    raise SystemExit(f"usage: {Path(sys.argv[0]).name} /path/to/quantum_ic_panorama_photosphere_white_24.png")

source_path = Path(sys.argv[1]).resolve()
if not source_path.is_file():
    raise SystemExit(f"source icon not found: {source_path}")
if sha256(source_path) != EXPECTED_SOURCE_SHA256:
    raise SystemExit(f"unexpected source icon: {source_path}")

project_root = Path(__file__).resolve().parents[1]
foreground_path = project_root / "assets/icon/photosphere-icon-native-depth-v2-foreground.png"
launcher_path = project_root / "assets/icon/photosphere-icon-native-depth-v2-launcher.png"
preview_path = project_root / "assets/icon/photosphere-icon-native-depth-v2-preview.png"

glyph = Image.open(source_path).convert("RGBA").resize(
    (GLYPH_SIZE, GLYPH_SIZE), Image.Resampling.LANCZOS
)

# Add four clipped facets to turn the panorama band's flat end caps into folded corners.
facet_layer = Image.new("RGBA", glyph.size, (0, 0, 0, 0))
facet_draw = ImageDraw.Draw(facet_layer)
facet_draw.polygon(scaled_polygon([(4, 36), (20, 31), (20, 43), (4, 48)]), fill=(205, 205, 205, 255))
facet_draw.polygon(scaled_polygon([(4, 50), (20, 57), (20, 65), (4, 60)]), fill=(132, 132, 132, 255))
facet_draw.polygon(scaled_polygon([(91, 36), (75, 31), (75, 43), (91, 48)]), fill=(205, 205, 205, 255))
facet_draw.polygon(scaled_polygon([(91, 50), (75, 57), (75, 65), (91, 60)]), fill=(132, 132, 132, 255))
facet_layer.putalpha(ImageChops.multiply(facet_layer.getchannel("A"), glyph.getchannel("A")))

styled_glyph = glyph.copy()
styled_glyph.alpha_composite(facet_layer)
offset = ((CANVAS_SIZE - GLYPH_SIZE) // 2,) * 2

# Shadow is deliberately restrained so it remains photographic rather than glossy.
shadow_alpha = styled_glyph.getchannel("A").filter(ImageFilter.GaussianBlur(14))
shadow_alpha = shadow_alpha.point(lambda value: round(value * 0.72))
shadow = Image.new("RGBA", styled_glyph.size, (0, 0, 0, 0))
shadow.putalpha(shadow_alpha)

foreground = Image.new("RGBA", (CANVAS_SIZE, CANVAS_SIZE), (0, 0, 0, 0))
foreground.alpha_composite(shadow, (offset[0], offset[1] + 12))
foreground.alpha_composite(styled_glyph, offset)
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
