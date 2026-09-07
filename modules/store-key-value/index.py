def store_key_value(store: dict, key: str, value) -> dict:
    if not isinstance(store, dict):
        store = {}
    store[key] = value
    return {"store": store, "stored": True}
