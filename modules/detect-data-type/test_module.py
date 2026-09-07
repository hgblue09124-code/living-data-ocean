import unittest
import os
import importlib.util

spec = importlib.util.spec_from_file_location("index", os.path.join(os.path.dirname(__file__), "index.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
detect_data_type = mod.detect_data_type

class TestDetectDataType(unittest.TestCase):
    def test_detect_json(self):
        res = detect_data_type('{"key": "val"}')
        self.assertEqual(res["detected_type"], "json")

    def test_detect_url(self):
        res = detect_data_type("https://example.com")
        self.assertEqual(res["detected_type"], "url")

if __name__ == "__main__":
    unittest.main()
