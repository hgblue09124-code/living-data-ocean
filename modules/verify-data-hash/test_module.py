import unittest
import os
import hashlib
import importlib.util

spec = importlib.util.spec_from_file_location("index", os.path.join(os.path.dirname(__file__), "index.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
verify_data_hash = mod.verify_data_hash

class TestVerifyDataHash(unittest.TestCase):
    def test_verify_sha256(self):
        data = "hello world"
        expected = hashlib.sha256(data.encode()).hexdigest()
        res = verify_data_hash(data, expected)
        self.assertTrue(res["match"])

if __name__ == "__main__":
    unittest.main()
