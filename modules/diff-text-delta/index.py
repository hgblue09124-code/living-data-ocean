import difflib

def diff_text_delta(text_a: str, text_b: str, from_name: str = "a", to_name: str = "b") -> dict:
    lines_a = text_a.splitlines(keepends=True)
    lines_b = text_b.splitlines(keepends=True)

    delta = list(difflib.unified_diff(lines_a, lines_b, fromfile=from_name, tofile=to_name))
    diff_str = "".join(delta)

    return {
        "diff": diff_str,
        "has_changes": len(delta) > 0
    }
