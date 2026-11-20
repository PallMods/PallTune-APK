#!/usr/bin/env python3
"""Sync PallTune README's SVG download counter with GitHub's real release API.

The only source for the number is the "download_count" attribute of the
"PallTune.apk" asset in the latest public release (no fabricated counters).
"""
import json
import os
from pathlib import Path
from urllib.request import Request, urlopen
from xml.sax.saxutils import escape

REPOSITORY = "PallMods/PallTune-APK"
ASSET_NAME = "PallTune.apk"
DESTINATION = Path("assets/downloads.svg")


def get_download_count():
    req = Request(
        f"https://api.github.com/repos/{REPOSITORY}/releases/latest",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "PallTune-README-Download-Counter",
            "X-GitHub-Api-Version": "2022-11-28",
            **(
                {"Authorization": f"Bearer {os.environ['GH_TOKEN']}"}
                if os.environ.get("GH_TOKEN")
                else {}
            ),
        },
    )
    with urlopen(req, timeout=30) as response:
        release = json.load(response)

    for asset in release.get("assets", []):
        if asset.get("name") == ASSET_NAME and asset.get("state") == "uploaded":
            count = asset["download_count"]
            if not isinstance(count, int) or count < 0:
                raise ValueError("GitHub API returned invalid download_count")
            return count, release["tag_name"]
    raise RuntimeError(
        "The latest published GitHub release has no uploaded PallTune.apk asset; "
        "the previous counter will remain unchanged."
    )


def make_badge(count):
    value = f"{count:,}"
    label = "APK DOWNLOADS"
    label_w = 128
    value_w = max(49, 29 + len(value) * 8)
    total_w = label_w + value_w
    value_x = label_w + value_w // 2

    # SVG is static text based on the GitHub API's real numeric value.
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{total_w}" height="24" viewBox="0 0 {total_w} 24" role="img" aria-label="{escape(label)}: {escape(value)}">
<title>{escape(label)}: {escape(value)} (GitHub Releases)</title>
<rect width="{total_w}" height="24" rx="6" fill="#171A1F"/>
<path d="M{label_w},0 H{total_w-6} Q{total_w},0 {total_w},6 V18 Q{total_w},24 {total_w-6},24 H{label_w} Z" fill="#424955"/>
<path d="M{label_w},2 V22" stroke="#68717C" stroke-width="1"/>
<text x="{label_w//2}" y="16" fill="#E2E6EB" text-anchor="middle" font-family="Verdana,DejaVu Sans,sans-serif" font-size="10.5" font-weight="700">{escape(label)}</text>
<text x="{value_x}" y="16.5" fill="#FFFFFF" text-anchor="middle" font-family="Verdana,DejaVu Sans,sans-serif" font-size="13" font-weight="700">{escape(value)}</text>
</svg>
"""


def main():
    count, release = get_download_count()
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    desired = make_badge(count)
    old = DESTINATION.read_text(encoding="utf-8") if DESTINATION.exists() else None
    if desired != old:
        DESTINATION.write_text(desired, encoding="utf-8")
        print(f"UPDATED: GitHub release {release}, {ASSET_NAME} = {count:,} downloads")
    else:
        print(f"UNCHANGED: GitHub release {release}, {ASSET_NAME} = {count:,} downloads")


if __name__ == "__main__":
    main()
