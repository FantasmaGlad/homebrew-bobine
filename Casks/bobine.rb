cask "bobine" do
  version "5.1.2"
  sha256 "e328bf20b3786d351fc5a64c72277676c80471194d87665fef50a82348c62306"

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
