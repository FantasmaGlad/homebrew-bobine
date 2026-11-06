#!/usr/bin/env python3
"""Écrit le cask Bobine, ou celui de l'assistant d'installation, pour une release Stable, à partir de son SHA256SUMS.

Usage : cask.py <SHA256SUMS> <tag Vx.y.z>                      (cask bobine, sur stdout)
        cask.py assistant <SHA256SUMS> <tag assistant-Vx.y.z>   (cask bobine-assistant, sur stdout)
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
    # La commande `bobine` existe depuis la 5.1.0 : BobineTray la sert quand il reçoit une sous-commande.
    major, minor, _ = (int(part) for part in version.split("."))
    command = (
        '\n  binary "#{appdir}/Bobine.app/Contents/MacOS/BobineTray", target: "bobine"'
        if (major, minor) >= (5, 1) else ""
    )
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

  app "Bobine.app"{command}
end
'''


def digest_of(sums_text: str, name: str) -> str:
    for line in sums_text.splitlines():
        match = re.fullmatch(r"([0-9a-fA-F]{64}) [ *](\S+)", line.strip())
        if match and match.group(2) == name:
            return match.group(1).lower()
    raise SystemExit(f"{name} absent de SHA256SUMS")


def assistant_cask(sums_text: str, tag: str) -> str:
    """L'assistant a sa propre release par Stable (assistant-Vx.y.z), jamais « Latest » : voir le dépôt Bobine."""
    if not re.fullmatch(r"assistant-V\d+\.\d+\.\d+", tag):
        raise SystemExit(f"tag Stable de l'assistant attendu (assistant-Vx.y.z) : {tag}")
    version = tag.removeprefix("assistant-V")
    digest = digest_of(sums_text, f"Bobine-Assistant-{version}-arm64.dmg")
    return f'''cask "bobine-assistant" do
  version "{version}"
  sha256 "{digest}"

  url "https://github.com/FantasmaGlad/Bobine/releases/download/assistant-V#{{version}}/Bobine-Assistant-#{{version}}-arm64.dmg"
  name "Bobine Assistant"
  desc "Installs Bobine on a dedicated mini PC over SSH"
  homepage "https://bobine.fit"

  livecheck do
    url "https://github.com/FantasmaGlad/Bobine/releases"
    regex(/assistant-V(\d+(?:\.\d+)+)/i)
    strategy :page_match
  end

  auto_updates true
  depends_on arch: :arm64

  app "Bobine Assistant.app"
  binary "#{{appdir}}/Bobine Assistant.app/Contents/MacOS/bobine-assistant"
end
'''


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "assistant":
        sys.stdout.write(assistant_cask(Path(sys.argv[2]).read_text(encoding="utf-8"), sys.argv[3]))
    elif len(sys.argv) == 3:
        sys.stdout.write(cask(Path(sys.argv[1]).read_text(encoding="utf-8"), sys.argv[2]))
    else:
        raise SystemExit(__doc__)
