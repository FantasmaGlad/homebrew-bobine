cask "bobine" do
  version "5.1.1"
  sha256 "510be27b52acb1d6b12c33f34a64d1e57f713f3d9b725a73f1574b957dd9d0e7"

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
