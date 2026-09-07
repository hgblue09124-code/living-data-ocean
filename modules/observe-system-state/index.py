import sys
import os
import platform

def observe_system_state(include_env: bool = False) -> dict:
    state = {
        "platform": platform.platform(),
        "python_version": sys.version,
        "pid": os.getpid(),
        "cwd": os.getcwd()
    }
    if include_env:
        state["environment"] = dict(os.environ)
    return state
