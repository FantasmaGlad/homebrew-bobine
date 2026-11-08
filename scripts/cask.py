#!/usr/bin/env python3
"""Écrit le cask Bobine, ou celui de Bobine Deploy, pour une release Stable, à partir de son SHA256SUMS.

Usage : cask.py <SHA256SUMS> <tag Vx.y.z>              (cask bobine, sur stdout)
        cask.py deploy <SHA256SUMS> <tag vx.y.z>       (cask bobine-deploy, dépôt FantasmaGlad/bobine-deploy, sur stdout)
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


def deploy_cask(sums_text: str, tag: str) -> str:
    """Bobine Deploy a son propre dépôt et ses tags vx.y.z ; une image par architecture."""
    if not re.fullmatch(r"v\d+\.\d+\.\d+", tag):
        raise SystemExit(f"tag Stable de Bobine Deploy attendu (vx.y.z) : {tag}")
    version = tag[1:]
    arm = digest_of(sums_text, f"Bobine-Deploy-{version}-arm64.dmg")
    intel = digest_of(sums_text, f"Bobine-Deploy-{version}-x64.dmg")
    return f'''cask "bobine-deploy" do
  arch arm: "arm64", intel: "x64"

  version "{version}"
  sha256 arm:   "{arm}",
         intel: "{intel}"

  url "https://github.com/FantasmaGlad/bobine-deploy/releases/download/v#{{version}}/Bobine-Deploy-#{{version}}-#{{arch}}.dmg"
  name "Bobine Deploy"
  desc "Install and maintain Bobine on the machines of your network"
  homepage "https://github.com/FantasmaGlad/bobine-deploy"

  livecheck do
    url :url
    strategy :github_latest
  end

  app "Bobine Deploy.app"
  binary "#{{appdir}}/Bobine Deploy.app/Contents/MacOS/bobine-deploy"
  binary "#{{appdir}}/Bobine Deploy.app/Contents/MacOS/bobine-deploy", target: "bdp"
end
'''


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "deploy":
        sys.stdout.write(deploy_cask(Path(sys.argv[2]).read_text(encoding="utf-8"), sys.argv[3]))
    elif len(sys.argv) == 3:
        sys.stdout.write(cask(Path(sys.argv[1]).read_text(encoding="utf-8"), sys.argv[2]))
    else:
        raise SystemExit(__doc__)
