import unittest
import os
import tempfile
import importlib.util

def import_index(module_dir):
    spec = importlib.util.spec_from_file_location("index", os.path.join(module_dir, "index.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

read_module = import_index(os.path.dirname(__file__))
read_file_content = read_module.read_file_content

class TestReadFileContent(unittest.TestCase):
    def test_read_text(self):
        with tempfile.NamedTemporaryFile("w", delete=False, encoding="utf-8") as f:
            f.write("Hello World")
            path = f.name
        try:
            res = read_file_content(path)
            self.assertEqual(res["content"], "Hello World")
            self.assertEqual(res["bytes_read"], 11)
        finally:
            os.remove(path)

    def test_read_binary(self):
        with tempfile.NamedTemporaryFile("wb", delete=False) as f:
            f.write(b"\x00\x01\x02")
            path = f.name
        try:
            res = read_file_content(path, binary=True)
            self.assertEqual(res["content"], b"\x00\x01\x02")
            self.assertEqual(res["bytes_read"], 3)
        finally:
            os.remove(path)

if __name__ == "__main__":
    unittest.main()
