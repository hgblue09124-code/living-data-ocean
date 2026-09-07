import os

def read_file_content(path: str, encoding: str = "utf-8", binary: bool = False) -> dict:
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    if binary:
        with open(path, "rb") as f:
            data = f.read()
        return {"content": data, "bytes_read": len(data)}
    else:
        with open(path, "r", encoding=encoding) as f:
            data = f.read()
        return {"content": data, "bytes_read": len(data.encode(encoding))}
