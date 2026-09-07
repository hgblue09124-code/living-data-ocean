def inspect_object_schema(obj) -> dict:
    obj_type = type(obj).__name__
    length = None
    if hasattr(obj, "__len__"):
        try:
            length = len(obj)
        except Exception:
            pass

    if isinstance(obj, dict):
        schema = {k: type(v).__name__ for k, v in obj.items()}
    elif isinstance(obj, (list, tuple, set)):
        schema = [type(item).__name__ for item in list(obj)[:10]]
    else:
        schema = str(obj)

    return {
        "type": obj_type,
        "schema": schema,
        "size_or_len": length
    }
