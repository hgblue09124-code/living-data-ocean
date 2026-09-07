import unittest
import os
import importlib.util

spec = importlib.util.spec_from_file_location("index", os.path.join(os.path.dirname(__file__), "index.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
check_condition_predicate = mod.check_condition_predicate

class TestCheckConditionPredicate(unittest.TestCase):
    def test_operators(self):
        self.assertTrue(check_condition_predicate(10, "gt", 5)["result"])
        self.assertTrue(check_condition_predicate("hello", "contains", "ell")["result"])
        self.assertFalse(check_condition_predicate("hello", "eq", "world")["result"])

if __name__ == "__main__":
    unittest.main()
