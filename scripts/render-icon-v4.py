#!/usr/bin/env python3
"""Render the deterministic Photo Sphere v4 launcher-icon concept."""

from pathlib import Path

from PIL import Image, ImageDraw


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "assets" / "icon" / "photosphere-icon-v4-minimal-preview.png"
SCALE = 4


def cubic(p0, p1, p2, p3, steps=160):
    points = []
    for index in range(steps + 1):
        t = index / steps
        u = 1 - t
        points.append(
            (
                u**3 * p0[0] + 3 * u**2 * t * p1[0] + 3 * u * t**2 * p2[0] + t**3 * p3[0],
                u**3 * p0[1] + 3 * u**2 * t * p1[1] + 3 * u * t**2 * p2[1] + t**3 * p3[1],
            )
        )
    return points


def quadratic(p0, p1, p2, steps=120):
    points = []
    for index in range(steps + 1):
        t = index / steps
        u = 1 - t
        points.append(
            (
                u**2 * p0[0] + 2 * u * t * p1[0] + t**2 * p2[0],
                u**2 * p0[1] + 2 * u * t * p1[1] + t**2 * p2[1],
            )
        )
    return points


def scaled(points):
    return [(round(x * SCALE), round(y * SCALE)) for x, y in points]


canvas = Image.new("RGBA", (1024 * SCALE, 1024 * SCALE), (0, 0, 0, 0))
draw = ImageDraw.Draw(canvas)

draw.rounded_rectangle(
    (32 * SCALE, 32 * SCALE, 992 * SCALE, 992 * SCALE),
    radius=224 * SCALE,
    fill="#151515",
)

upper = cubic((276, 405), (326, 248), (698, 248), (748, 405))
lower = cubic((276, 619), (326, 776), (698, 776), (748, 619))
draw.line(scaled(upper), fill="#F3F3F3", width=76 * SCALE, joint="curve")
draw.line(scaled(lower), fill="#F3F3F3", width=76 * SCALE, joint="curve")

outer_top = quadratic((242, 405), (512, 326), (782, 405))
outer_bottom = quadratic((782, 619), (512, 698), (242, 619))
draw.polygon(scaled(outer_top + outer_bottom), fill="#F7F7F7")

inner_top = quadratic((320, 461), (512, 409), (704, 461))
inner_bottom = quadratic((704, 563), (512, 615), (320, 563))
draw.polygon(scaled(inner_top + inner_bottom), fill="#151515")

canvas.resize((1024, 1024), Image.Resampling.LANCZOS).save(OUTPUT)
print(OUTPUT)
