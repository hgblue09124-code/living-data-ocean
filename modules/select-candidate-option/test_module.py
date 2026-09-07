import unittest
import os
import importlib.util

spec = importlib.util.spec_from_file_location("index", os.path.join(os.path.dirname(__file__), "index.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
select_candidate_option = mod.select_candidate_option

class TestSelectCandidateOption(unittest.TestCase):
    def test_select_by_key(self):
        opts = [{"name": "a", "score": 10}, {"name": "b", "score": 90}]
        res = select_candidate_option(opts, criterion_key="score")
        self.assertTrue(res["found"])
        self.assertEqual(res["selected"]["name"], "b")

if __name__ == "__main__":
    unittest.main()
