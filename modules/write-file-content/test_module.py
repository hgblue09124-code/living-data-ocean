import unittest
import os
import tempfile
import importlib.util

def import_index(module_dir):
    spec = importlib.util.spec_from_file_location("index", os.path.join(module_dir, "index.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

write_module = import_index(os.path.dirname(__file__))
write_file_content = write_module.write_file_content

class TestWriteFileContent(unittest.TestCase):
    def test_write_text(self):
        tmpdir = tempfile.mkdtemp()
        path = os.path.join(tmpdir, "test.txt")
        try:
            res = write_file_content(path, "Hello Write")
            self.assertTrue(res["success"])
            self.assertTrue(os.path.exists(path))
            with open(path, "r", encoding="utf-8") as f:
                self.assertEqual(f.read(), "Hello Write")
        finally:
            if os.path.exists(path):
                os.remove(path)
            os.rmdir(tmpdir)

if __name__ == "__main__":
    unittest.main()
