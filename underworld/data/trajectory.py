"""
Định nghĩa cấu trúc dữ liệu Trajectory lưu trữ chuỗi chuyển đổi trạng thái của mô phỏng.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from underworld.interface.observation import Observation
from underworld.interface.action import Action


@dataclass
class TrajectoryStep:
    """
    Một bước chuyển đổi trong chuỗi Trajectory:
    state_t -> observation_t -> action_t -> state_t+1
    """
    step: int
    state_before: Dict[str, Any]
    observation: Dict[str, Any]
    action: Optional[List[Dict[str, Any]]]
    state_after: Dict[str, Any]

    def to_dict(self) -> Dict[str, Any]:
        """Chuyển đổi TrajectoryStep thành dict để xuất ra JSON/JSONL."""
        return {
            "step": self.step,
            "state_before": self.state_before,
            "observation": self.observation,
            "action": self.action,
            "state_after": self.state_after
        }


@dataclass
class Trajectory:
    """
    Chuỗi các bước mô phỏng Trajectory đại diện cho một phiên chạy của Underworld.
    """
    trajectory_id: str
    steps: List[TrajectoryStep] = field(default_factory=list)

    def add_step(
        self,
        step: int,
        state_before: Any,
        observation: Observation,
        action: Optional[List[Action]],
        state_after: Any
    ) -> None:
        """Thêm một bước simulation vào Trajectory."""
        actions_dict = [act.to_dict() for act in action] if action else None

        sb_dict = state_before.to_dict() if hasattr(state_before, "to_dict") else state_before
        sa_dict = state_after.to_dict() if hasattr(state_after, "to_dict") else state_after
        obs_dict = observation.to_dict() if hasattr(observation, "to_dict") else observation

        traj_step = TrajectoryStep(
            step=step,
            state_before=sb_dict,
            observation=obs_dict,
            action=actions_dict,
            state_after=sa_dict
        )
        self.steps.append(traj_step)

    def to_dict(self) -> Dict[str, Any]:
        """Chuyển đổi toàn bộ Trajectory thành dict."""
        return {
            "trajectory_id": self.trajectory_id,
            "total_steps": len(self.steps),
            "steps": [s.to_dict() for s in self.steps]
        }
