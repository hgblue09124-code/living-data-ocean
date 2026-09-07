def select_candidate_option(candidates: list, criterion_key: str = None, default=None) -> dict:
    if not candidates:
        return {"selected": default, "selected_index": -1, "found": False}

    if criterion_key:
        best_index = -1
        best_val = None
        for idx, item in enumerate(candidates):
            if isinstance(item, dict) and criterion_key in item:
                val = item[criterion_key]
                if best_val is None or val > best_val:
                    best_val = val
                    best_index = idx
        if best_index >= 0:
            return {"selected": candidates[best_index], "selected_index": best_index, "found": True}

    return {"selected": candidates[0], "selected_index": 0, "found": True}
