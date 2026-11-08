cask "bobine-deploy" do
  arch arm: "arm64", intel: "x64"

  version "0.1.0"
  sha256 arm:   "273620804121df929f8997576ce00ea9a1c8141f6b8a805b1f5a14cae977f685",
         intel: "1ee4bdd08986ec7886333c8e6fd2e55535fce353eb08cfdc0b549f7c06555cd5"

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
  binary "#{appdir}/Bobine Deploy.app/Contents/MacOS/bobine-deploy", target: "bdp"
end
