import unittest
import os
import importlib.util

spec = importlib.util.spec_from_file_location("index", os.path.join(os.path.dirname(__file__), "index.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
transform_data_mapping = mod.transform_data_mapping

class TestTransformDataMapping(unittest.TestCase):
    def test_transform(self):
        source = {"first_name": "John", "last_name": "Doe"}
        mapping = {"firstName": "first_name", "lastName": "last_name"}
        res = transform_data_mapping(source, mapping)
        self.assertEqual(res["transformed"], {"firstName": "John", "lastName": "Doe"})

if __name__ == "__main__":
    unittest.main()
