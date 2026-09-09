"""UI Module hiển thị Tổng quan Trạng thái Thế giới (World State View)."""

from typing import Dict, Any, Optional, Callable
from underworld.modules.ui.base import UIModule


class WorldStateViewModule(UIModule):
    """UI Module chuyên trách hiển thị các chỉ số môi trường và thời gian của World."""

    def __init__(self):
        super().__init__(
            module_id="ui_world_state_view",
            title="🌍 Tổng Quan Thế Giới (World State)",
            category="view"
        )

    def render_web_dict(self, world_state: Dict[str, Any]) -> Dict[str, Any]:
        tick = world_state.get("time_step", 0)
        env = world_state.get("environment", {})
        weather = env.get("weather", "N/A")

        resources = env.get("resources", {})
        resource_val = resources.get("food", resources.get("tài_nguyên", 0.0)) if isinstance(resources, dict) else 0.0

        humans_raw = world_state.get("human_states", world_state.get("humans", {}))
        humans_count = len(humans_raw)
        events_count = len(world_state.get("events", []))

        return {
            "module_id": self.module_id,
            "title": self.title,
            "category": self.category,
            "type": "world_state_summary",
            "data": {
                "tick": tick,
                "weather": weather,
                "resource_level": round(resource_val, 2),
                "humans_count": humans_count,
                "events_count": events_count
            }
        }
