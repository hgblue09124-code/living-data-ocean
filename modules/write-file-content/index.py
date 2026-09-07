import os

def write_file_content(path: str, content: str | bytes, mode: str = "w", encoding: str = "utf-8") -> dict:
    dirname = os.path.dirname(path)
    if dirname and not os.path.exists(dirname):
        os.makedirs(dirname, exist_ok=True)

    if isinstance(content, bytes):
        write_mode = "wb" if "w" in mode else "ab"
        with open(path, write_mode) as f:
            bytes_written = f.write(content)
    elif isinstance(content, str):
        write_mode = "w" if "w" in mode else "a"
        with open(path, write_mode, encoding=encoding) as f:
            bytes_written = f.write(content)
    else:
        raise TypeError("Content must be string or bytes")

    return {
        "path": path,
        "bytes_written": bytes_written,
        "success": True
    }
