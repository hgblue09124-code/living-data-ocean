"""
Lớp lưu trữ trạng thái dữ liệu (State Representation) cho HumanState và WorldState.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any, Optional


@dataclass
class HumanState:
    """
    Lưu trữ trạng thái nội tại của một Human tại một thời điểm t.
    """
    id: str
    position: Tuple[int, int] = (0, 0)
    status: str = "nghỉ_ngơi"
    needs: Dict[str, float] = field(default_factory=lambda: {
        "năng_lượng": 100.0,
        "đói": 0.0,
        "xã_hội": 50.0
    })
    goals: List[str] = field(default_factory=lambda: ["khám_phá"])
    memory: List[Dict[str, Any]] = field(default_factory=list)
    action_history: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Chuyển đổi trạng thái Human thành dict để serialization."""
        return {
            "id": self.id,
            "position": list(self.position),
            "status": self.status,
            "needs": dict(self.needs),
            "goals": list(self.goals),
            "memory": list(self.memory),
            "action_history": list(self.action_history),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HumanState":
        """Khôi phục trạng thái Human từ dict."""
        return cls(
            id=data["id"],
            position=tuple(data.get("position", (0, 0))),
            status=data.get("status", "nghỉ_ngơi"),
            needs=data.get("needs", {"năng_lượng": 100.0, "đói": 0.0, "xã_hội": 50.0}),
            goals=data.get("goals", ["khám_phá"]),
            memory=data.get("memory", []),
            action_history=data.get("action_history", [])
        )


@dataclass
class WorldState:
    """
    Lưu trữ trạng thái toàn cảnh của Underworld tại thời điểm t.
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
