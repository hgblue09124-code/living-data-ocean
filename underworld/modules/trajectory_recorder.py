"""
Mô-đun Atomic ghi nhận lịch sử mô phỏng (TrajectoryRecorderModule).
"""

from typing import Optional, List, Dict, Any
from underworld.interface.observation import Observation
from underworld.interface.action import Action
from underworld.data.trajectory import Trajectory


class TrajectoryRecorderModule:
    """
    Trách nhiệm: Ghi nhận từng bước chuyển đổi (state_before, observation, action, state_after) vào Trajectory.
    """

    def record_step(
        self,
        trajectory: Trajectory,
        step: int,
        state_before: Any,
        observation: Observation,
        action: Optional[List[Action]],
        state_after: Any
    ) -> None:
        """
        Thêm một bước chuyển đổi trạng thái vào Trajectory.
        """
        trajectory.add_step(
            step=step,
            state_before=state_before,
            observation=observation,
            action=action,
            state_after=state_after
        )
