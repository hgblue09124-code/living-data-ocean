import unittest
import os
import importlib.util

spec = importlib.util.spec_from_file_location("index", os.path.join(os.path.dirname(__file__), "index.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
plan_step_decomposition = mod.plan_step_decomposition

class TestPlanStepDecomposition(unittest.TestCase):
    def test_plan(self):
        res = plan_step_decomposition("Build Feature", ["Step 1", "Step 2"])
        self.assertEqual(len(res["plan_steps"]), 2)
        self.assertEqual(res["plan_steps"][0]["title"], "Step 1")

if __name__ == "__main__":
    unittest.main()
