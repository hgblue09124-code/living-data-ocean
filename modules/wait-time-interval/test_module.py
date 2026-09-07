import unittest
import os
import importlib.util

spec = importlib.util.spec_from_file_location("index", os.path.join(os.path.dirname(__file__), "index.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
wait_time_interval = mod.wait_time_interval

class TestWaitTimeInterval(unittest.TestCase):
    def test_wait(self):
        res = wait_time_interval(0.01)
        self.assertTrue(res["completed"])
        self.assertGreaterEqual(res["elapsed"], 0.009)

if __name__ == "__main__":
    unittest.main()
