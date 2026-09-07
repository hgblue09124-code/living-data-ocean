import unittest
import os
import importlib.util

spec = importlib.util.spec_from_file_location("index", os.path.join(os.path.dirname(__file__), "index.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
validate_schema_dict = mod.validate_schema_dict

class TestValidateSchemaDict(unittest.TestCase):
    def test_validate_success(self):
        schema = {"required": ["id"], "types": {"id": "int", "name": "str"}}
        res = validate_schema_dict({"id": 123, "name": "Test"}, schema)
        self.assertTrue(res["valid"])
        self.assertEqual(res["errors"], [])

    def test_validate_failure(self):
        schema = {"required": ["id"], "types": {"id": "int"}}
        res = validate_schema_dict({"id": "123"}, schema)
        self.assertFalse(res["valid"])
        self.assertIn("Field 'id' expected type 'int', got 'str'", res["errors"])

if __name__ == "__main__":
    unittest.main()
