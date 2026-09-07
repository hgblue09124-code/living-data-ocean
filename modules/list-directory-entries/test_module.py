import unittest
import os
import tempfile
import importlib.util

def import_index(module_dir):
    spec = importlib.util.spec_from_file_location("index", os.path.join(module_dir, "index.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

list_module = import_index(os.path.dirname(__file__))
list_directory_entries = list_module.list_directory_entries

class TestListDirectoryEntries(unittest.TestCase):
    def test_list_entries(self):
        tmpdir = tempfile.mkdtemp()
        file1 = os.path.join(tmpdir, "a.txt")
        with open(file1, "w") as f:
            f.write("test")
        try:
            res = list_directory_entries(tmpdir)
            names = [e["name"] for e in res["entries"]]
            self.assertIn("a.txt", names)
        finally:
            os.remove(file1)
            os.rmdir(tmpdir)

if __name__ == "__main__":
    unittest.main()
