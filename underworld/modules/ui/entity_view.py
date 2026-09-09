"""UI Module hiển thị Danh sách Thực thể / Con người (Entity View)."""

import tkinter as tk
from tkinter import ttk
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

    def render_tk(
        self,
        parent_widget: Any,
        world_state: Dict[str, Any],
        callbacks: Optional[Dict[str, Callable]] = None
    ) -> Any:
        frame = ttk.LabelFrame(parent_widget, text=self.title, padding=10)

        columns = ("id", "position", "energy", "hunger", "health", "action")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=5)

        tree.heading("id", text="ID Human")
        tree.heading("position", text="Vị trí (x, y)")
        tree.heading("energy", text="Năng lượng")
        tree.heading("hunger", text="Mức đói")
        tree.heading("health", text="Sức khỏe")
        tree.heading("action", text="Hành động gần nhất")

        tree.column("id", width=100, anchor="center")
        tree.column("position", width=100, anchor="center")
        tree.column("energy", width=90, anchor="center")
        tree.column("hunger", width=90, anchor="center")
        tree.column("health", width=90, anchor="center")
        tree.column("action", width=180, anchor="w")

        # Hỗ trợ cả danh sách dict và human_states dict
        humans_raw = world_state.get("human_states", world_state.get("humans", {}))
        if isinstance(humans_raw, dict):
            humans = list(humans_raw.values())
        else:
            humans = humans_raw

        for human in humans:
            if hasattr(human, "to_dict"):
                human = human.to_dict()

            h_id = human.get("id", "N/A")
            pos = human.get("position", (0, 0))
            needs = human.get("needs", {})
            energy = f"{needs.get('năng_lượng', needs.get('energy', 0.0)):.1f}"
            hunger = f"{needs.get('đói', needs.get('hunger', 0.0)):.1f}"
            health = f"{needs.get('sức_khỏe', needs.get('health', 100.0)):.1f}"

            act_hist = human.get("action_history", [])
            last_action = act_hist[-1] if act_hist else human.get("status", "N/A")

            tree.insert("", "end", values=(h_id, str(pos), energy, hunger, health, last_action))

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        return frame
