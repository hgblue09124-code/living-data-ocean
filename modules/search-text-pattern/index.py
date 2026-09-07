import re

def search_text_pattern(text: str, query: str, is_regex: bool = False, case_sensitive: bool = True) -> dict:
    if not query:
        return {"matches": []}

    lines = text.splitlines()
    matches = []

    flags = 0 if case_sensitive else re.IGNORECASE

    if not is_regex:
        pattern = re.escape(query)
    else:
        pattern = query

    compiled = re.compile(pattern, flags)

    for line_idx, line in enumerate(lines, start=1):
        for match in compiled.finditer(line):
            matches.append({
                "line_number": line_idx,
                "line_text": line,
                "start": match.start(),
                "end": match.end()
            })

    return {"matches": matches}
