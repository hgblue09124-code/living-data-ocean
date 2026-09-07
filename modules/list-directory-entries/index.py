import os

def list_directory_entries(path: str = ".", recursive: bool = False, include_hidden: bool = False) -> dict:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Path does not exist: {path}")
    if not os.path.isdir(path):
        raise NotADirectoryError(f"Path is not a directory: {path}")

    entries = []
    if recursive:
        for root, dirs, files in os.walk(path):
            if not include_hidden:
                dirs[:] = [d for d in dirs if not d.startswith(".")]
                files = [f for f in files if not f.startswith(".")]
            for name in dirs + files:
                full_path = os.path.join(root, name)
                is_dir = os.path.isdir(full_path)
                entries.append({
                    "name": name,
                    "path": full_path,
                    "is_dir": is_dir,
                    "size": 0 if is_dir else os.path.getsize(full_path)
                })
    else:
        for name in os.listdir(path):
            if not include_hidden and name.startswith("."):
                continue
            full_path = os.path.join(path, name)
            is_dir = os.path.isdir(full_path)
            entries.append({
                "name": name,
                "path": full_path,
                "is_dir": is_dir,
                "size": 0 if is_dir else os.path.getsize(full_path)
            })

    return {"entries": entries}
