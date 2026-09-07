def validate_schema_dict(data: dict, schema: dict) -> dict:
    errors = []
    if not isinstance(data, dict):
        return {"valid": False, "errors": ["Input data is not a dictionary"]}

    required = schema.get("required", [])
    for field in required:
        if field not in data:
            errors.append(f"Missing required field: '{field}'")

    types = schema.get("types", {})
    type_map = {
        "str": str,
        "int": int,
        "float": float,
        "bool": bool,
        "dict": dict,
        "list": list
    }

    for field, expected_type_str in types.items():
        if field in data and data[field] is not None:
            expected_type = type_map.get(expected_type_str)
            if expected_type and not isinstance(data[field], expected_type):
                actual_type = type(data[field]).__name__
                errors.append(f"Field '{field}' expected type '{expected_type_str}', got '{actual_type}'")

    return {
        "valid": len(errors) == 0,
        "errors": errors
    }
