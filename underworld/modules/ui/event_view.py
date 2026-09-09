"""UI Module hiển thị Sự kiện Thế giới (Event View)."""

import tkinter as tk
from tkinter import ttk
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

    def render_tk(
        self,
        parent_widget: Any,
        world_state: Dict[str, Any],
        callbacks: Optional[Dict[str, Callable]] = None
    ) -> Any:
        frame = ttk.LabelFrame(parent_widget, text=self.title, padding=10)

        events = world_state.get("events", [])
        if not events:
            lbl_empty = ttk.Label(frame, text="Hiện không có sự kiện đặc biệt nào đang diễn ra.", font=("Helvetica", 10, "italic"))
            lbl_empty.pack(anchor="w", padx=5, pady=5)
        else:
            columns = ("type", "detail")
            tree = ttk.Treeview(frame, columns=columns, show="headings", height=3)
            tree.heading("type", text="Loại Sự Kiện")
            tree.heading("detail", text="Nội dung / Tác động")

            tree.column("type", width=180, anchor="w")
            tree.column("detail", width=400, anchor="w")

            for evt in events:
                evt_type = evt.get("type", evt.get("name", "N/A"))
                detail = evt.get("chi_tiết", str(evt.get("payload", {})))
                tree.insert("", "end", values=(evt_type, detail))

            tree.pack(fill="both", expand=True)

        return frame
