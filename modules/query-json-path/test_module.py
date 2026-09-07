import unittest
import os
import importlib.util

spec = importlib.util.spec_from_file_location("index", os.path.join(os.path.dirname(__file__), "index.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
query_json_path = mod.query_json_path

class TestQueryJsonPath(unittest.TestCase):
    def test_query_nested(self):
        data = {"users": [{"name": "Bob"}, {"name": "Alice"}]}
        res = query_json_path(data, "users.1.name")
        self.assertTrue(res["found"])
        self.assertEqual(res["value"], "Alice")

    def test_query_missing(self):
        data = {"a": 1}
        res = query_json_path(data, "a.b", default=404)
        self.assertFalse(res["found"])
        self.assertEqual(res["value"], 404)

if __name__ == "__main__":
    unittest.main()
