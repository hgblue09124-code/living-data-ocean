import unittest
import os
import importlib.util

spec = importlib.util.spec_from_file_location("index", os.path.join(os.path.dirname(__file__), "index.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
store_key_value = mod.store_key_value

class TestStoreKeyValue(unittest.TestCase):
    def test_store(self):
        s = {}
        res = store_key_value(s, "session_id", "xyz789")
        self.assertTrue(res["stored"])
        self.assertEqual(res["store"]["session_id"], "xyz789")

if __name__ == "__main__":
    unittest.main()
