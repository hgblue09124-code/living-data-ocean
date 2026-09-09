"""
Định nghĩa đối tượng Observation - Ranh giới quan sát thế giới cho External Agent.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional


@dataclass
class Observation:
    """
    Ranh giới góc nhìn (Observation) cung cấp thông tin thế giới cho External Agent.
    """
    time_step: int
    visible_humans: List[Dict[str, Any]] = field(default_factory=list)
    environment_summary: Dict[str, Any] = field(default_factory=dict)
    recent_events: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_world_state(
        cls,
        world_state: Any,
        target_human_id: Optional[str] = None
    ) -> "Observation":
        """
        Tạo Observation từ một WorldState.
        """
        visible = []
        human_states = getattr(world_state, "human_states", {})
        if isinstance(human_states, dict):
            for hid, hstate in human_states.items():
                if target_human_id is None or target_human_id == hid:
                    if hasattr(hstate, "id"):
                        visible.append({
                            "id": hstate.id,
                            "position": hstate.position,
                            "status": hstate.status,
                            "needs": dict(hstate.needs),
                            "goals": list(hstate.goals)
                        })
                    elif isinstance(hstate, dict):
                        visible.append({
                            "id": hstate.get("id"),
                            "position": hstate.get("position"),
                            "status": hstate.get("status"),
                            "needs": hstate.get("needs"),
                            "goals": hstate.get("goals")
                        })

        env = getattr(world_state, "environment", {}) if hasattr(world_state, "environment") else {}
        events = getattr(world_state, "events", []) if hasattr(world_state, "events") else []
        time_step = getattr(world_state, "time_step", 0) if hasattr(world_state, "time_step") else 0

        return cls(
            time_step=time_step,
            visible_humans=visible,
            environment_summary=dict(env),
            recent_events=list(events)
        )

    def to_dict(self) -> Dict[str, Any]:
        """Chuyển đổi Observation thành dict."""
        return {
            "time_step": self.time_step,
            "visible_humans": self.visible_humans,
            "environment_summary": self.environment_summary,
            "recent_events": self.recent_events
        }
