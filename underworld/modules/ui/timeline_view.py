"""UI Module hiển thị Dòng thời gian / Lịch sử Simulation (Timeline View)."""

import tkinter as tk
from tkinter import ttk
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

    def render_tk(
        self,
        parent_widget: Any,
        world_state: Dict[str, Any],
        callbacks: Optional[Dict[str, Callable]] = None
    ) -> Any:
        frame = ttk.LabelFrame(parent_widget, text=self.title, padding=10)

        txt_log = tk.Text(frame, height=5, wrap="word", font=("Courier", 9))
        txt_log.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=txt_log.yview)
        txt_log.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        tick = world_state.get("time_step", 0)
        humans_raw = world_state.get("human_states", world_state.get("humans", {}))
        if isinstance(humans_raw, dict):
            humans = list(humans_raw.values())
        else:
            humans = humans_raw

        events = world_state.get("events", [])

        log_lines = [
            f"[Tick {tick}] Mô phỏng đang chạy...",
            f" - Con người active: {len(humans)} cá thể.",
            f" - Event tích cực: {len(events)} sự kiện.",
        ]
        for h in humans:
            if hasattr(h, "to_dict"):
                h = h.to_dict()
            h_id = h.get("id", "N/A")
            h_pos = h.get("position", (0, 0))
            h_needs = h.get("needs", {})
            h_energy = h_needs.get("năng_lượng", h_needs.get("energy", 0.0))
            log_lines.append(f" - [{h_id}] vị trí {h_pos} | Năng lượng: {h_energy:.1f}")

        txt_log.insert("1.0", "\n".join(log_lines))
        txt_log.config(state="disabled")

        return frame
