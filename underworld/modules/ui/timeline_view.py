"""UI Module hiển thị Dòng thời gian / Lịch sử Simulation (Timeline View)."""

from typing import Dict, Any, Optional, Callable
from underworld.modules.ui.base import UIModule


class TimelineViewModule(UIModule):
    """UI Module chuyên trách hiển thị nhật ký diễn biến theo thời gian (Timeline Log)."""

    def __init__(self):
        super().__init__(
            module_id="ui_timeline_view",
            title="📜 Nhật Ký Dòng Thời Gian (Simulation Timeline)",
            category="timeline"
        )

    def render_web_dict(self, world_state: Dict[str, Any]) -> Dict[str, Any]:
        tick = world_state.get("time_step", 0)
        humans_raw = world_state.get("human_states", world_state.get("humans", {}))
        if isinstance(humans_raw, dict):
            humans = list(humans_raw.values())
        else:
            humans = humans_raw

        events = world_state.get("events", [])

        log_lines = [
            f"[Tick {tick}] Mô phỏng đang diễn ra tự chủ.",
            f" - Con người active: {len(humans)} cá thể.",
            f" - Ghi nhận: {len(events)} sự kiện bước này.",
        ]
        for h in humans:
            if hasattr(h, "to_dict"):
                h = h.to_dict()
            h_id = h.get("id", "N/A")
            h_pos = h.get("position", (0, 0))
            h_needs = h.get("needs", {})
            h_energy = h_needs.get("năng_lượng", h_needs.get("energy", 0.0))
            log_lines.append(f" - [{h_id}] vị trí {h_pos} | Năng lượng: {h_energy:.1f}")

        return {
            "module_id": self.module_id,
            "title": self.title,
            "category": self.category,
            "type": "timeline_log",
            "data": {
                "tick": tick,
                "log_lines": log_lines
            }
        }
