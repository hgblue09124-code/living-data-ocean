import unittest
import os
import importlib.util

spec = importlib.util.spec_from_file_location("index", os.path.join(os.path.dirname(__file__), "index.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
invoke_callable_handler = mod.invoke_callable_handler

class TestInvokeCallableHandler(unittest.TestCase):
    def test_invoke_success(self):
        res = invoke_callable_handler(lambda a, b: a + b, args=(2, 3))
        self.assertTrue(res["success"])
        self.assertEqual(res["result"], 5)

    def test_invoke_not_callable(self):
        res = invoke_callable_handler("not_a_func")
        self.assertFalse(res["success"])

if __name__ == "__main__":
    unittest.main()
