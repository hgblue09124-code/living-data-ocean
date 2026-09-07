import json

def parse_json_structured(data: str | bytes, fallback=None) -> dict:
    if isinstance(data, bytes):
        data = data.decode("utf-8")
    try:
        parsed = json.loads(data)
        return {"parsed": parsed, "success": True, "error": None}
    except Exception as e:
        if fallback is not None:
            return {"parsed": fallback, "success": False, "error": str(e)}
        return {"parsed": None, "success": False, "error": str(e)}
