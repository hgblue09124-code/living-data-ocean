"""
Định nghĩa đối tượng Observation - Ranh giới quan sát thế giới cho External Agent.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from underworld.world.state import WorldState


@dataclass
class Observation:
    """
    Ranh giới góc nhìn (Observation) cung cấp thông tin thế giới cho External Agent.

    Agent bên ngoài KHÔNG được phép truy cập trực tiếp toàn bộ internal state
    hoặc biến nội tại của World, mà chỉ được nhận thông tin qua đối tượng Observation này.

    Attributes:
        time_step (int): Thời điểm t của thế giới.
        visible_humans (List[Dict[str, Any]]): Trạng thái các Human mà Agent có thể quan sát.
        environment_summary (Dict[str, Any]): Tóm tắt điều kiện môi trường.
        recent_events (List[Dict[str, Any]]): Các sự kiện quan sát được trong lượt vừa qua.
    """
    time_step: int
    visible_humans: List[Dict[str, Any]] = field(default_factory=list)
    environment_summary: Dict[str, Any] = field(default_factory=dict)
    recent_events: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_world_state(
        cls,
        world_state: WorldState,
        target_human_id: Optional[str] = None
    ) -> "Observation":
        """
        Tạo Observation từ một WorldState.

        Nếu target_human_id được chỉ định, chỉ quan sát trạng thái liên quan đến Human đó.
        Nếu không chỉ định, trả về tổng quan toàn bộ các Human trong thế giới.
        """
        visible = []
        for hid, hstate in world_state.human_states.items():
            if target_human_id is None or target_human_id == hid:
                visible.append({
                    "id": hstate.id,
                    "position": hstate.position,
                    "status": hstate.status,
                    "needs": dict(hstate.needs),
                    "goals": list(hstate.goals)
                })

        return cls(
            time_step=world_state.time_step,
            visible_humans=visible,
            environment_summary=dict(world_state.environment),
            recent_events=list(world_state.events)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Chuyển đổi Observation thành dict để xuất dữ liệu/xuất trajectory."""
        return {
            "time_step": self.time_step,
            "visible_humans": self.visible_humans,
            "environment_summary": self.environment_summary,
            "recent_events": self.recent_events
        }
