"""
Mô-đun ranh giới giao tiếp (Interface) giữa Underworld và External Agent.
"""

from underworld.interface.observation import Observation
from underworld.interface.action import Action

__all__ = ["Observation", "Action"]
