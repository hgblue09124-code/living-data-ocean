import re

def check_condition_predicate(value, operator: str, target) -> dict:
    op = operator.lower()
    try:
        if op == "eq":
            res = value == target
        elif op == "neq":
            res = value != target
        elif op == "gt":
            res = value > target
        elif op == "gte":
            res = value >= target
        elif op == "lt":
            res = value < target
        elif op == "lte":
            res = value <= target
        elif op == "in":
            res = value in target
        elif op == "contains":
            res = target in value
        elif op == "regex":
            res = bool(re.search(str(target), str(value)))
        else:
            raise ValueError(f"Unknown operator: {operator}")
        return {"result": res}
    except Exception:
        return {"result": False}
