#!/usr/bin/env python3
"""Import the owner's PallTune 4.3.5 APK from public MediaFire.
Validate size and SHA256 against the original user-supplied APK.
"""
import base64
import hashlib
import html
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

PAGE = "https://www.mediafire.com/file/nuwd6rktohfqhr0/PallTune+V4.3.5.apk/file"
EXPECTED_SIZE = 39361232
EXPECTED_SHA256 = "f6058f96eabda3987d8f0548e0538a03bf4ed8659bdc1599d0348857f9ac638d"
OUT = Path("PallTune.apk")


def get_direct_url():
    variants = [
        PAGE,
        "https://www.mediafire.com/file/nuwd6rktohfqhr0/",
        "https://www.mediafire.com/?nuwd6rktohfqhr0",
        "https://www.mediafire.com/file/nuwd6rktohfqhr0/PallTune%20V4.3.5.apk/file",
    ]
    errors = []
    for page in variants:
        try:
            response = requests.get(page, headers={"User-Agent": "Mozilla/5.0"}, timeout=45)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            button = soup.select_one("#downloadButton")
            candidates = []
            if button:
                scrambled = button.get("data-scrambled-url")
                if scrambled:
                    candidates.append(base64.b64decode(scrambled).decode("utf-8"))
                candidates.append(button.get("href"))
            for node in soup.select('a[aria-label="Download file"], a[href*="download"][href*="mediafire.com"]'):
                candidates.append(node.get("href"))
            candidates.extend(re.findall(r'https?://download[0-9]+\.mediafire\.com[^" <]+', response.text))
            for candidate in candidates:
                if candidate:
                    candidate = html.unescape(candidate)
                    parsed = urlparse(candidate)
                    if parsed.scheme == "https" and parsed.hostname and re.fullmatch(r"download\d*\.mediafire\.com", parsed.hostname):
                        return candidate
            errors.append(f"{page} => no download button")
        except Exception as error:
            errors.append(f"{page} => {error}")
    raise RuntimeError("All MediaFire URLs failed: " + " | ".join(errors))

def main():
    url = get_direct_url()
    with requests.get(url, stream=True, timeout=(30, 180), headers={"User-Agent": "Mozilla/5.0"}) as response:
        response.raise_for_status()
        with OUT.open("wb") as dest:
            for chunk in response.iter_content(1024 * 1024):
                if chunk:
                    dest.write(chunk)

    size = OUT.stat().st_size
    digest = hashlib.sha256(OUT.read_bytes()).hexdigest()
    with OUT.open("rb") as src:
        header = src.read(4)
    if size != EXPECTED_SIZE or digest != EXPECTED_SHA256 or header != bytes([80, 75, 3, 4]):
        OUT.unlink(missing_ok=True)
        raise RuntimeError("File does not match the original APK; refusing to publish.")
    print(f"Verified APK: {size} bytes; SHA256: {digest}")


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Import failed:", error, file=sys.stderr)
        sys.exit(1)
