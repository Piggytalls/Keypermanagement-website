#!/usr/bin/env python3
"""
Derive web-ready logo/favicon assets from the source brand logo.

The brand logo (brand_assents/keyper_logo_centered.png) ships as a flat
opaque PNG — a full-bleed background rectangle behind the wordmark, not a
transparent cutout. That breaks two things a site needs:

  1. A transparent logo to place on any background (e.g. inverted white
     on the dark footer) — a flat-bg PNG just shows as a solid block.
  2. A square favicon showing just the house+key mark, not the whole wide
     wordmark lockup squashed into a tiny box.

This script derives both, deterministically, from the one source file:
  - assets/img/keyper-logo.png              (verbatim copy of the source)
  - assets/img/keyper-logo-transparent.png  (background color-keyed out,
                                              cropped tight to content)
  - assets/img/favicon-512.png / -32.png / -16.png / apple-touch-icon.png
    (square crops of just the house+key mark, background intact)

Re-run whenever the source logo file changes. Safe to re-run any time —
it always regenerates from the source, never from its own output.

Usage:
    python3 tools/prepare_brand_assets.py
    python3 tools/prepare_brand_assets.py --source path/to/logo.png
"""

import argparse
import math
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = ROOT / "brand_assents" / "keyper_logo_centered.png"
DEFAULT_OUT_DIR = ROOT / "assets" / "img"

# Icon-mark search window, tuned to keyper_logo_centered.png's layout
# (house+key glyph sits left of the wordmark, above the tagline). If the
# source logo's proportions change materially, re-tune these.
ICON_SEARCH_Y = (400, 560)
ICON_SEARCH_X_MAX = 760

FAVICON_SIZES = {
    "favicon-512.png": 512,
    "apple-touch-icon.png": 180,
    "favicon-32.png": 32,
    "favicon-16.png": 16,
}


def _dist(c1, c2):
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(c1, c2)))


def make_transparent(img: Image.Image, min_d=8.0, max_d=60.0) -> Image.Image:
    """Color-key out the flat background, cropped tight to remaining content."""
    img = img.convert("RGBA")
    px = img.load()
    w, h = img.size
    bg = px[5, 5][:3]

    for y in range(h):
        for x in range(w):
            r, g, b, a = px[x, y]
            d = _dist((r, g, b), bg)
            if d <= min_d:
                alpha = 0
            elif d >= max_d:
                alpha = 255
            else:
                alpha = int(255 * (d - min_d) / (max_d - min_d))
            px[x, y] = (r, g, b, alpha)

    bbox = img.getbbox()
    if bbox:
        pad = 14
        l, t, r, b = bbox
        l, t = max(0, l - pad), max(0, t - pad)
        r, b = min(w, r + pad), min(h, b + pad)
        img = img.crop((l, t, r, b))
    return img


def crop_icon_mark(img: Image.Image) -> Image.Image:
    """Find and square-crop just the house+key glyph (excludes wordmark/tagline)."""
    rgb = img.convert("RGB")
    w, h = rgb.size
    px = rgb.load()
    bg = px[5, 5]

    y0, y1 = ICON_SEARCH_Y
    x_limit = min(ICON_SEARCH_X_MAX, w)

    minx, miny, maxx, maxy = w, h, 0, 0
    for y in range(y0, min(y1, h)):
        for x in range(x_limit):
            if _dist(px[x, y], bg) > 18:
                minx, miny = min(minx, x), min(miny, y)
                maxx, maxy = max(maxx, x), max(maxy, y)

    if maxx <= minx or maxy <= miny:
        raise ValueError(
            "Could not find the icon mark within the configured search "
            "window — adjust ICON_SEARCH_Y / ICON_SEARCH_X_MAX for the new logo."
        )

    pad = int(max(maxx - minx, maxy - miny) * 0.28)
    minx, miny = minx - pad, miny - pad
    maxx, maxy = maxx + pad, maxy + pad
    side = max(maxx - minx, maxy - miny)
    cx, cy = (minx + maxx) // 2, (miny + maxy) // 2
    half = side // 2
    return rgb.crop((cx - half, cy - half, cx + half, cy + half))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=str(DEFAULT_SOURCE))
    parser.add_argument("--out-dir", default=str(DEFAULT_OUT_DIR))
    args = parser.parse_args()

    source = Path(args.source)
    out_dir = Path(args.out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    if not source.exists():
        raise SystemExit(f"Source logo not found: {source}")

    print(f"Preparing brand assets from {source.relative_to(ROOT)}...")
    original = Image.open(source)

    verbatim_path = out_dir / "keyper-logo.png"
    original.convert("RGB").save(verbatim_path)
    print(f"  wrote {verbatim_path.relative_to(ROOT)}")

    transparent = make_transparent(original)
    transparent_path = out_dir / "keyper-logo-transparent.png"
    transparent.save(transparent_path)
    print(f"  wrote {transparent_path.relative_to(ROOT)} ({transparent.size[0]}x{transparent.size[1]})")

    icon_mark = crop_icon_mark(original)
    for filename, size in FAVICON_SIZES.items():
        resized = icon_mark.resize((size, size), Image.LANCZOS)
        out_path = out_dir / filename
        resized.save(out_path)
        print(f"  wrote {out_path.relative_to(ROOT)} ({size}x{size})")

    print("Done.")


if __name__ == "__main__":
    main()
