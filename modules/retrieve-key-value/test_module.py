import unittest
import os
import importlib.util

spec = importlib.util.spec_from_file_location("index", os.path.join(os.path.dirname(__file__), "index.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
retrieve_key_value = mod.retrieve_key_value

class TestRetrieveKeyValue(unittest.TestCase):
    def test_retrieve(self):
        store = {"token": "abc12345"}
        res = retrieve_key_value(store, "token")
        self.assertTrue(res["found"])
        self.assertEqual(res["value"], "abc12345")

if __name__ == "__main__":
    unittest.main()
