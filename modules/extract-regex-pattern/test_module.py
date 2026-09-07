import unittest
import os
import importlib.util

spec = importlib.util.spec_from_file_location("index", os.path.join(os.path.dirname(__file__), "index.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
extract_regex_pattern = mod.extract_regex_pattern

class TestExtractRegexPattern(unittest.TestCase):
    def test_extract_simple(self):
        res = extract_regex_pattern("foo123 bar456", r"\d+")
        self.assertEqual(res["matches"], ["123", "456"])

    def test_extract_named(self):
        res = extract_regex_pattern("User: Alice, ID: 42", r"User: (?P<name>\w+), ID: (?P<id>\d+)")
        self.assertEqual(res["matches"], [{"name": "Alice", "id": "42"}])

if __name__ == "__main__":
    unittest.main()
