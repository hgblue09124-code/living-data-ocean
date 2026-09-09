"""UI Module chứa Bảng Điều khiển Mô phỏng (Simulation Control View)."""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Optional, Callable
from underworld.modules.ui.base import UIModule


class SimulationControlViewModule(UIModule):
    """UI Module chuyên trách cung cấp các nút bấm điều khiển simulation (Play, Pause, Step, Admin Command)."""

    def __init__(self):
        super().__init__(
            module_id="ui_simulation_control_view",
            title="🎮 Bảng Điều Khiển Mô Phỏng (Simulation Control)",
            category="control"
        )

    def render_tk(
        self,
        parent_widget: Any,
        world_state: Dict[str, Any],
        callbacks: Optional[Dict[str, Callable]] = None
    ) -> Any:
        frame = ttk.LabelFrame(parent_widget, text=self.title, padding=10)
        cbs = callbacks or {}

        btn_step = ttk.Button(
            frame,
            text="⏭️ Bước Tiếp (1 Tick)",
            command=cbs.get("on_step")
        )
        btn_step.grid(row=0, column=0, padx=5, pady=5)

        btn_run_10 = ttk.Button(
            frame,
            text="⏩ Chạy 10 Ticks",
            command=lambda: cbs.get("on_run_n", lambda n: None)(10)
        )
        btn_run_10.grid(row=0, column=1, padx=5, pady=5)

        btn_rain = ttk.Button(
            frame,
            text="🌧️ Quản Trị Viên: Gửi Mưa",
            command=lambda: cbs.get("on_admin_weather", lambda w: None)("Mưa lớn")
        )
        btn_rain.grid(row=0, column=2, padx=5, pady=5)

        btn_clear = ttk.Button(
            frame,
            text="☀️ Quản Trị Viên: Nắng Đẹp",
            command=lambda: cbs.get("on_admin_weather", lambda w: None)("Nắng nhẹ")
        )
        btn_clear.grid(row=0, column=3, padx=5, pady=5)

        btn_quit = ttk.Button(
            frame,
            text="🛑 Dừng Mô Phỏng",
            command=cbs.get("on_stop")
        )
        btn_quit.grid(row=0, column=4, padx=5, pady=5)

        return frame
