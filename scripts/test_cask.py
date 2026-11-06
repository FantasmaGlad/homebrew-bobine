import unittest

from cask import assistant_cask, cask

SUMS = "a" * 64 + "  Bobine-9.9.9.dmg\n" + "b" * 64 + "  install.sh\n"


class CaskTests(unittest.TestCase):
    def test_version_and_digest_come_from_the_release(self):
        text = cask(SUMS, "V9.9.9")
        self.assertIn('version "9.9.9"', text)
        self.assertIn(f'sha256 "{"a" * 64}"', text)
        self.assertIn("depends_on arch: :arm64", text)

    def test_command_is_linked_from_5_1_0(self):
        self.assertIn('binary "#{appdir}/Bobine.app/Contents/MacOS/BobineTray", target: "bobine"', cask(SUMS, "V9.9.9"))
        old = "a" * 64 + "  Bobine-5.0.7.dmg\n"
        self.assertNotIn("binary", cask(old, "V5.0.7"))

    def test_rolling_tag_or_missing_image_is_refused(self):
        with self.assertRaises(SystemExit):
            cask(SUMS, "canary")
        with self.assertRaises(SystemExit):
            cask("b" * 64 + "  install.sh\n", "V9.9.9")


    def test_assistant_cask_comes_from_its_own_release(self):
        sums = "c" * 64 + "  Bobine-Assistant-5.1.1-arm64.dmg\n" + "d" * 64 + "  Bobine-Assistant-5.1.1-arm64.app.tar.gz\n"
        text = assistant_cask(sums, "assistant-V5.1.1")
        self.assertIn('cask "bobine-assistant" do', text)
        self.assertIn('sha256 "' + "c" * 64 + '"', text)
        self.assertIn("releases/download/assistant-V#{version}/Bobine-Assistant-#{version}-arm64.dmg", text)
        self.assertIn('binary "#{appdir}/Bobine Assistant.app/Contents/MacOS/bobine-assistant"', text)
        self.assertIn("auto_updates true", text)
        with self.assertRaises(SystemExit):
            assistant_cask(sums, "V5.1.1")


if __name__ == "__main__":
    unittest.main()
