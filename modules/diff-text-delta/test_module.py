import unittest
import os
import importlib.util

spec = importlib.util.spec_from_file_location("index", os.path.join(os.path.dirname(__file__), "index.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
diff_text_delta = mod.diff_text_delta

class TestDiffTextDelta(unittest.TestCase):
    def test_diff_with_changes(self):
        res = diff_text_delta("hello\nworld", "hello\nthere")
        self.assertTrue(res["has_changes"])
        self.assertIn("-world", res["diff"])
        self.assertIn("+there", res["diff"])

if __name__ == "__main__":
    unittest.main()
