import unittest

from cask import cask

SUMS = "a" * 64 + "  Bobine-9.9.9.dmg\n" + "b" * 64 + "  install.sh\n"


class CaskTests(unittest.TestCase):
    def test_version_and_digest_come_from_the_release(self):
        text = cask(SUMS, "V9.9.9")
        self.assertIn('version "9.9.9"', text)
        self.assertIn(f'sha256 "{"a" * 64}"', text)
        self.assertIn("depends_on arch: :arm64", text)

    def test_rolling_tag_or_missing_image_is_refused(self):
        with self.assertRaises(SystemExit):
            cask(SUMS, "canary")
        with self.assertRaises(SystemExit):
            cask("b" * 64 + "  install.sh\n", "V9.9.9")


if __name__ == "__main__":
    unittest.main()
