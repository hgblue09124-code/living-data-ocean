import re

def extract_regex_pattern(text: str, pattern: str, flags: int = 0) -> dict:
    compiled = re.compile(pattern, flags)
    matches = []
    for match in compiled.finditer(text):
        groupdict = match.groupdict()
        if groupdict:
            matches.append(groupdict)
        elif match.groups():
            matches.append(list(match.groups()))
        else:
            matches.append(match.group(0))
    return {"matches": matches}
