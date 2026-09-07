import unittest
import os
import importlib.util

spec = importlib.util.spec_from_file_location("index", os.path.join(os.path.dirname(__file__), "index.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
parse_json_structured = mod.parse_json_structured

class TestParseJsonStructured(unittest.TestCase):
    def test_parse_valid(self):
        res = parse_json_structured('{"a": 1}')
        self.assertTrue(res["success"])
        self.assertEqual(res["parsed"], {"a": 1})

    def test_parse_invalid(self):
        res = parse_json_structured('{a: 1}', fallback={})
        self.assertFalse(res["success"])
        self.assertEqual(res["parsed"], {})

if __name__ == "__main__":
    unittest.main()
