cask "bobine" do
  version "5.0.7"
  sha256 "f48504717bde641fc0b7f30fa9b88b79b42e43dcf59e2080e3c1f3bdd332abea"

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
end
