#!/usr/bin/env python3
"""Build smaller, lower-frame-rate animated WebP versions for PallTune website.

Source GIF files remain unchanged for the public README. This script writes
separate WebP assets for the website so animations consume less bandwidth
and decoding work on mobile devices.
"""
from pathlib import Path
from PIL import Image, features

ASSETS = Path("assets")
NAMES = ["hero", "player", "playlist", "lyrics", "together"]

if not features.check("webp_anim"):
    raise RuntimeError("Pillow does not support animated WebP in this runner")

for name in NAMES:
    source = ASSETS / f"palltune-{name}.gif"
    dest = ASSETS / f"palltune-{name}-site.webp"
    with Image.open(source) as animation:
        frames = []
        durations = []
        original_frames = animation.n_frames
        # Keep every second frame and preserve the original overall duration.
        for index in range(0, original_frames, 2):
            animation.seek(index)
            frame = animation.convert("RGB")
            if name == "hero":
                frame.thumbnail((760, 260), Image.Resampling.LANCZOS)
            else:
                frame.thumbnail((500, 205), Image.Resampling.LANCZOS)
            duration = int(animation.info.get("duration", 95) or 95)
            if index + 1 < original_frames:
                animation.seek(index + 1)
                duration += int(animation.info.get("duration", 95) or 95)
            frames.append(frame)
            durations.append(max(80, duration))
        frames[0].save(
            dest, format="WEBP", save_all=True,
            append_images=frames[1:], duration=durations, loop=0,
            method=6, quality=55, minimize_size=True, kmin=3, kmax=10,
        )
    with Image.open(dest) as result:
        assert result.n_frames > 1, "WebP must stay animated"
    before = source.stat().st_size
    after = dest.stat().st_size
    print(f"{name}: {before:,} -> {after:,} bytes ({after/before:.1%}) | {original_frames} -> {len(frames)} frames")
