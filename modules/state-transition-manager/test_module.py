import unittest
import os
import importlib.util

spec = importlib.util.spec_from_file_location("index", os.path.join(os.path.dirname(__file__), "index.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
state_transition_manager = mod.state_transition_manager

class TestStateTransitionManager(unittest.TestCase):
    def test_transition(self):
        rules = {"idle": {"start": "running"}, "running": {"stop": "idle"}}
        res = state_transition_manager("idle", "start", rules)
        self.assertTrue(res["allowed"])
        self.assertEqual(res["next_state"], "running")

if __name__ == "__main__":
    unittest.main()
