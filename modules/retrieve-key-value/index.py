def retrieve_key_value(store: dict, key: str, default=None) -> dict:
    if not isinstance(store, dict):
        return {"value": default, "found": False}
    if key in store:
        return {"value": store[key], "found": True}
    return {"value": default, "found": False}
