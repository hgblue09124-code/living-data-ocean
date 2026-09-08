"""
Mô-đun quản lý không gian World và trạng thái WorldState của Underworld.
"""

from underworld.world.state import WorldState


def __getattr__(name: str):
    if name == "World":
        from underworld.composition.world import World
        return World
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["WorldState", "World"]
