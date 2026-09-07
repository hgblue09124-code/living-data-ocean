import os
import fnmatch

def find_file_path(root_path: str, pattern: str = "*", max_depth: int = -1) -> dict:
    if not os.path.exists(root_path):
        return {"matches": []}

    matches = []
    root_path = os.path.abspath(root_path)
    base_depth = root_path.count(os.sep)

    for root, dirs, files in os.walk(root_path):
        current_depth = root.count(os.sep) - base_depth
        if max_depth >= 0 and current_depth > max_depth:
            dirs[:] = []
            continue

        for name in files + dirs:
            if fnmatch.fnmatch(name, pattern):
                matches.append(os.path.join(root, name))

    return {"matches": matches}
