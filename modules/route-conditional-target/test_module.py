import unittest
import os
import importlib.util

spec = importlib.util.spec_from_file_location("index", os.path.join(os.path.dirname(__file__), "index.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
route_conditional_target = mod.route_conditional_target

class TestRouteConditionalTarget(unittest.TestCase):
    def test_route(self):
        routes = [
            {"key": "type", "operator": "eq", "value": "alert", "target": "slack_channel"},
            {"key": "priority", "operator": "eq", "value": "high", "target": "pagerduty"}
        ]
        res = route_conditional_target({"type": "alert"}, routes)
        self.assertEqual(res["target"], "slack_channel")

if __name__ == "__main__":
    unittest.main()
