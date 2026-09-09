"""UI Module hiển thị Sự kiện Thế giới (Event View)."""

from typing import Dict, Any, Optional, Callable
from underworld.modules.ui.base import UIModule


class EventViewModule(UIModule):
    """UI Module chuyên trách hiển thị các sự kiện môi trường xảy ra trong World."""

    def __init__(self):
        super().__init__(
            module_id="ui_event_view",
            title="⚡ Sự Kiện Môi Trường (World Events)",
            category="view"
        )

    def render_web_dict(self, world_state: Dict[str, Any]) -> Dict[str, Any]:
        events = world_state.get("events", [])
        event_list = []
        for evt in events:
            evt_type = evt.get("type", evt.get("name", "N/A"))
            detail = evt.get("chi_tiết", str(evt.get("payload", {})))
            time_step = evt.get("time_step", world_state.get("time_step", 0))
            event_list.append({
                "type": evt_type,
                "detail": detail,
                "time_step": time_step
            })

        return {
            "module_id": self.module_id,
            "title": self.title,
            "category": self.category,
            "type": "event_list",
            "data": {
                "events": event_list
            }
        }
