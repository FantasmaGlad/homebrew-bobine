cask "bobine" do
  version "5.2.2"
  sha256 "e27b9db5227c2e510fc93279e49faca3e05798ba62246d910845e56c47fabc40"

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
