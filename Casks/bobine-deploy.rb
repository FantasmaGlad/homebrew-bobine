cask "bobine-deploy" do
  arch arm: "arm64", intel: "x64"

  version "0.0.1"
  sha256 arm:   "b426c8f78d135f17850efbe866335ee3933c8bfffda86a1ec89d9a012ee8d215",
         intel: "1fdbb30df0e346ad41b2e0d12ad44ee45850c66ff2eac582a03952698f21bc87"

  url "https://github.com/FantasmaGlad/bobine-deploy/releases/download/v#{version}/Bobine-Deploy-#{version}-#{arch}.dmg"
  name "Bobine Deploy"
  desc "Install and maintain Bobine on the machines of your network"
  homepage "https://github.com/FantasmaGlad/bobine-deploy"

  livecheck do
    url :url
    strategy :github_latest
  end

  app "Bobine Deploy.app"
  binary "#{appdir}/Bobine Deploy.app/Contents/MacOS/bobine-deploy"
end
