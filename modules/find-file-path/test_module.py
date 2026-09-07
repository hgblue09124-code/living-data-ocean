import unittest
import os
import tempfile
import importlib.util

def import_index(module_dir):
    spec = importlib.util.spec_from_file_location("index", os.path.join(module_dir, "index.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

find_module = import_index(os.path.dirname(__file__))
find_file_path = find_module.find_file_path

class TestFindFilePath(unittest.TestCase):
    def test_find_file(self):
        tmpdir = tempfile.mkdtemp()
        sub = os.path.join(tmpdir, "sub")
        os.mkdir(sub)
        file1 = os.path.join(sub, "sample.py")
        with open(file1, "w") as f:
            f.write("# py")
        try:
            res = find_file_path(tmpdir, pattern="*.py")
            self.assertEqual(len(res["matches"]), 1)
            self.assertEqual(res["matches"][0], file1)
        finally:
            os.remove(file1)
            os.rmdir(sub)
            os.rmdir(tmpdir)

if __name__ == "__main__":
    unittest.main()
