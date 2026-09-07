def compare_object_equality(left, right, strict: bool = True) -> dict:
    if left == right:
        return {"equal": True, "difference_summary": None}

    if type(left) != type(right) and strict:
        return {
            "equal": False,
            "difference_summary": f"Type mismatch: left is {type(left).__name__}, right is {type(right).__name__}"
        }

    return {
        "equal": False,
        "difference_summary": f"Values do not match: {left} != {right}"
    }
