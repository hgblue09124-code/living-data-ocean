def query_json_path(data, path: str, default=None) -> dict:
    if not path:
        return {"value": data, "found": True}

    parts = path.split(".")
    curr = data
    for part in parts:
        if isinstance(curr, dict) and part in curr:
            curr = curr[part]
        elif isinstance(curr, (list, tuple)):
            try:
                idx = int(part)
                curr = curr[idx]
            except (ValueError, IndexError):
                return {"value": default, "found": False}
        else:
            return {"value": default, "found": False}

    return {"value": curr, "found": True}
