"""
Mô-đun quản lý thực thể Human và trạng thái của Human trong Underworld.
"""

from underworld.human.state import HumanState


def __getattr__(name: str):
    if name == "Human":
        from underworld.composition.human import Human
        return Human
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["HumanState", "Human"]
