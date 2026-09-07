def route_conditional_target(payload: dict, routes: list, default_target: str = "default") -> dict:
    if not isinstance(payload, dict):
        return {"target": default_target, "matched_rule": None}

    for rule in routes:
        key = rule.get("key")
        operator = rule.get("operator", "eq")
        val = rule.get("value")
        target = rule.get("target")

        if key in payload:
            actual = payload[key]
            match = False
            if operator == "eq" and actual == val:
                match = True
            elif operator == "neq" and actual != val:
                match = True
            elif operator == "contains" and val in actual:
                match = True
            elif operator == "in" and actual in val:
                match = True

            if match:
                return {"target": target, "matched_rule": rule}

    return {"target": default_target, "matched_rule": None}
