import unittest
import os
import importlib.util

spec = importlib.util.spec_from_file_location("index", os.path.join(os.path.dirname(__file__), "index.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
compare_object_equality = mod.compare_object_equality

class TestCompareObjectEquality(unittest.TestCase):
    def test_compare_equal(self):
        res = compare_object_equality({"a": 1}, {"a": 1})
        self.assertTrue(res["equal"])

    def test_compare_not_equal(self):
        res = compare_object_equality({"a": 1}, {"a": 2})
        self.assertFalse(res["equal"])

if __name__ == "__main__":
    unittest.main()
