"""
Định nghĩa trạng thái toàn cục của thế giới Underworld tại thời điểm t.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any
from underworld.human.state import HumanState


@dataclass
class WorldState:
    """
    Lưu trữ trạng thái toàn cảnh của Underworld tại thời điểm t.

    Attributes:
        time_step (int): Thời gian mô phỏng t hiện tại.
        human_states (Dict[str, HumanState]): Trạng thái của tất cả Human trong thế giới.
        environment (Dict[str, Any]): Trạng thái môi trường (kích thước thế giới, tài nguyên...).
        events (List[Dict[str, Any]]): Các sự kiện phát sinh trong lượt t.
    """
    time_step: int = 0
    human_states: Dict[str, HumanState] = field(default_factory=dict)
    environment: Dict[str, Any] = field(default_factory=dict)
    events: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Chuyển đổi trạng thái WorldState thành dict để xuất dữ liệu."""
        return {
            "time_step": self.time_step,
            "human_states": {
                hid: hstate.to_dict() for hid, hstate in self.human_states.items()
            },
            "environment": dict(self.environment),
            "events": list(self.events)
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "WorldState":
        """Khôi phục trạng thái WorldState từ dict."""
        human_states = {
            hid: HumanState.from_dict(hdata)
            for hid, hdata in data.get("human_states", {}).items()
        }
        return cls(
            time_step=data.get("time_step", 0),
            human_states=human_states,
            environment=data.get("environment", {}),
            events=data.get("events", [])
        )
