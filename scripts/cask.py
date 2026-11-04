#!/usr/bin/env python3
"""Écrit le cask Bobine pour une release Stable, à partir de son SHA256SUMS.

Usage : cask.py <SHA256SUMS> <tag Vx.y.z>   (le cask sort sur stdout)
"""
import re
import sys
from pathlib import Path


def cask(sums_text: str, tag: str) -> str:
    if not re.fullmatch(r"V\d+\.\d+\.\d+", tag):
        raise SystemExit(f"tag Stable attendu (Vx.y.z) : {tag}")
    version = tag[1:]
    name = f"Bobine-{version}.dmg"
    digest = None
    for line in sums_text.splitlines():
        match = re.fullmatch(r"([0-9a-fA-F]{64}) [ *](\S+)", line.strip())
        if match and match.group(2) == name:
            digest = match.group(1).lower()
    if digest is None:
        raise SystemExit(f"{name} absent de SHA256SUMS")
    return f'''cask "bobine" do
  version "{version}"
  sha256 "{digest}"

  url "https://github.com/FantasmaGlad/Bobine/releases/download/V#{{version}}/Bobine-#{{version}}.dmg"
  name "Bobine"
  desc "Offline-first video playout for gyms and studios"
  homepage "https://bobine.fit"

  livecheck do
    url :url
    strategy :github_latest
  end

  depends_on arch: :arm64

  app "Bobine.app"
end
'''


if __name__ == "__main__":
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    sys.stdout.write(cask(Path(sys.argv[1]).read_text(encoding="utf-8"), sys.argv[2]))
