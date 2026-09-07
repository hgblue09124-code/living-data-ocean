import unittest
import os
import importlib.util

spec = importlib.util.spec_from_file_location("index", os.path.join(os.path.dirname(__file__), "index.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
observe_system_state = mod.observe_system_state

class TestObserveSystemState(unittest.TestCase):
    def test_observe(self):
        res = observe_system_state(include_env=False)
        self.assertIn("platform", res)
        self.assertIn("pid", res)

if __name__ == "__main__":
    unittest.main()
