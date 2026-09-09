"""
Mô-đun Atomic xây dựng Observation cho External Agent (ObservationBuilderModule).
"""

from typing import Optional, Any
from underworld.interface.observation import Observation


class ObservationBuilderModule:
    """
    Trách nhiệm: Xây dựng đối tượng Observation từ WorldState snapshot cho External Agent.
    """

    def build_observation(
        self,
        world_state: Any,
        target_human_id: Optional[str] = None
    ) -> Observation:
        """
        Tạo Observation từ WorldState.
        """
        return Observation.from_world_state(world_state, target_human_id=target_human_id)
