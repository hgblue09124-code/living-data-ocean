def transform_data_mapping(data: dict, mapping: dict) -> dict:
    result = {}
    for target_key, source_key in mapping.items():
        if isinstance(source_key, str):
            result[target_key] = data.get(source_key)
        elif callable(source_key):
            result[target_key] = source_key(data)
        else:
            result[target_key] = source_key
    return {"transformed": result}
