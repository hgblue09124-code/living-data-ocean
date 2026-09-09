"""UI Module hiển thị Tổng quan Trạng thái Thế giới (World State View)."""

import tkinter as tk
from tkinter import ttk
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

    def render_tk(
        self,
        parent_widget: Any,
        world_state: Dict[str, Any],
        callbacks: Optional[Dict[str, Callable]] = None
    ) -> Any:
        frame = ttk.LabelFrame(parent_widget, text=self.title, padding=10)

        tick = world_state.get("time_step", 0)
        env = world_state.get("environment", {})
        weather = env.get("weather", "N/A")

        # Sửa key "resources" thay vì "resource_level"
        resources = env.get("resources", {})
        resource_val = resources.get("food", resources.get("tài_nguyên", 0.0)) if isinstance(resources, dict) else 0.0

        humans_count = len(world_state.get("human_states", world_state.get("humans", {})))
        events_count = len(world_state.get("events", []))

        lbl_tick = ttk.Label(frame, text=f"⏱️ Thời gian (Tick): {tick}", font=("Helvetica", 11, "bold"))
        lbl_tick.grid(row=0, column=0, sticky="w", padx=5, pady=2)

        lbl_weather = ttk.Label(frame, text=f"🌤️ Thời tiết: {weather}")
        lbl_weather.grid(row=0, column=1, sticky="w", padx=15, pady=2)

        lbl_resource = ttk.Label(frame, text=f"🌱 Tài nguyên: {resource_val:.2f}")
        lbl_resource.grid(row=1, column=0, sticky="w", padx=5, pady=2)

        lbl_humans = ttk.Label(frame, text=f"👥 Số lượng Con người: {humans_count}")
        lbl_humans.grid(row=1, column=1, sticky="w", padx=15, pady=2)

        lbl_events = ttk.Label(frame, text=f"⚡ Sự kiện hiện tại: {events_count}")
        lbl_events.grid(row=1, column=2, sticky="w", padx=15, pady=2)

        return frame
