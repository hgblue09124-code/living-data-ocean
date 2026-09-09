"""UI Module hiển thị Danh sách Thực thể / Con người (Entity View)."""

from typing import Dict, Any, Optional, Callable
from underworld.modules.ui.base import UIModule


class EntityViewModule(UIModule):
    """UI Module chuyên trách hiển thị danh sách và trạng thái chi tiết của các Human."""

    def __init__(self):
        super().__init__(
            module_id="ui_entity_view",
            title="👥 Danh Sách Con Người (Human Entities)",
            category="view"
        )

    def render_web_dict(self, world_state: Dict[str, Any]) -> Dict[str, Any]:
        humans_raw = world_state.get("human_states", world_state.get("humans", {}))
        if isinstance(humans_raw, dict):
            humans = list(humans_raw.values())
        else:
            humans = humans_raw

        entity_list = []
        for human in humans:
            if hasattr(human, "to_dict"):
                human = human.to_dict()

            h_id = human.get("id", "N/A")
            pos = human.get("position", (0, 0))
            needs = human.get("needs", {})
            energy = round(needs.get("năng_lượng", needs.get("energy", 0.0)), 1)
            hunger = round(needs.get("đói", needs.get("hunger", 0.0)), 1)
            health = round(needs.get("sức_khỏe", needs.get("health", 100.0)), 1)

            act_hist = human.get("action_history", [])
            last_action = act_hist[-1] if act_hist else human.get("status", "N/A")

            entity_list.append({
                "id": h_id,
                "position": list(pos),
                "energy": energy,
                "hunger": hunger,
                "health": health,
                "last_action": last_action,
                "status": human.get("status", "N/A")
            })

        return {
            "module_id": self.module_id,
            "title": self.title,
            "category": self.category,
            "type": "entity_table",
            "data": {
                "entities": entity_list
            }
        }
