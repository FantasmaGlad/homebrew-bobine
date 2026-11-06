cask "bobine" do
  version "5.1.0"
  sha256 "53bc780a4580f1846579f0a5468554f39b71c77c77f3cc20643357e9588cdbb8"

  url "https://github.com/FantasmaGlad/Bobine/releases/download/V#{version}/Bobine-#{version}.dmg"
  name "Bobine"
  desc "Offline-first video playout for gyms and studios"
  homepage "https://bobine.fit"

  livecheck do
    url :url
    strategy :github_latest
  end

  depends_on arch: :arm64

  app "Bobine.app"
  binary "#{appdir}/Bobine.app/Contents/MacOS/BobineTray", target: "bobine"
end
