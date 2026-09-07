import unittest
import os
import importlib.util

spec = importlib.util.spec_from_file_location("index", os.path.join(os.path.dirname(__file__), "index.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
inspect_object_schema = mod.inspect_object_schema

class TestInspectObjectSchema(unittest.TestCase):
    def test_inspect_dict(self):
        res = inspect_object_schema({"name": "Alice", "age": 30})
        self.assertEqual(res["type"], "dict")
        self.assertEqual(res["schema"], {"name": "str", "age": "int"})
        self.assertEqual(res["size_or_len"], 2)

if __name__ == "__main__":
    unittest.main()
