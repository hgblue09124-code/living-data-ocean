"""
Re-export EventLoop từ underworld.runtime.event_loop để bảo toàn tính tương thích ngược.
"""

from underworld.runtime.event_loop import EventLoop

__all__ = ["EventLoop"]
