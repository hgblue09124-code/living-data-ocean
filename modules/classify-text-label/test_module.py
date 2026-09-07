import unittest
import os
import importlib.util

spec = importlib.util.spec_from_file_location("index", os.path.join(os.path.dirname(__file__), "index.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
classify_text_label = mod.classify_text_label

class TestClassifyTextLabel(unittest.TestCase):
    def test_classify(self):
        cats = {
            "bug": ["error", "exception", "crash"],
            "feature": ["add", "request", "feature"]
        }
        res = classify_text_label("System crash with error code 500", cats)
        self.assertEqual(res["label"], "bug")

if __name__ == "__main__":
    unittest.main()
