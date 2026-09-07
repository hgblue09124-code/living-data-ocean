import json
import re

def detect_data_type(value) -> dict:
    if isinstance(value, dict):
        return {"detected_type": "dict", "confidence": 1.0}
    if isinstance(value, list):
        return {"detected_type": "list", "confidence": 1.0}
    if isinstance(value, int) and not isinstance(value, bool):
        return {"detected_type": "int", "confidence": 1.0}
    if isinstance(value, float):
        return {"detected_type": "float", "confidence": 1.0}
    if isinstance(value, bool):
        return {"detected_type": "bool", "confidence": 1.0}

    if isinstance(value, str):
        val = value.strip()
        if (val.startswith("{") and val.endswith("}")) or (val.startswith("[") and val.endswith("]")):
            try:
                json.loads(val)
                return {"detected_type": "json", "confidence": 0.95}
            except Exception:
                pass

        if re.match(r"^https?://[^\s]+$", val):
            return {"detected_type": "url", "confidence": 0.9}

        if re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", val):
            return {"detected_type": "email", "confidence": 0.9}

        if val.isdigit():
            return {"detected_type": "numeric_string", "confidence": 0.85}

        return {"detected_type": "str", "confidence": 1.0}

    return {"detected_type": "unknown", "confidence": 0.5}
