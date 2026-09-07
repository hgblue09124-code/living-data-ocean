import unittest
import os
import importlib.util

spec = importlib.util.spec_from_file_location("index", os.path.join(os.path.dirname(__file__), "index.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
search_text_pattern = mod.search_text_pattern

class TestSearchTextPattern(unittest.TestCase):
    def test_search_simple(self):
        text = "line one\nline two error\nline three"
        res = search_text_pattern(text, "error")
        self.assertEqual(len(res["matches"]), 1)
        self.assertEqual(res["matches"][0]["line_number"], 2)

if __name__ == "__main__":
    unittest.main()
