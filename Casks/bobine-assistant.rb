cask "bobine-assistant" do
  version "5.1.1"
  sha256 "6e28c4b0e9ea074d2354e05e19417fb155a530f1bce725297784743d4da3184f"

  url "https://github.com/FantasmaGlad/Bobine/releases/download/assistant-V#{version}/Bobine-Assistant-#{version}-arm64.dmg"
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
  binary "#{appdir}/Bobine Assistant.app/Contents/MacOS/bobine-assistant"
end
