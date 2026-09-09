"""UIProgram — Chương trình Giao diện Đồ họa được tổng hợp từ UI Modules.

UIProgram nhận một danh sách các UI Modules đã được lọc và sắp xếp, sau đó
dựng (render) giao diện đồ họa Tkinter tương ứng mà không hard-code cấu trúc layout.
"""

import tkinter as tk
from tkinter import ttk
from typing import List, Dict, Any, Optional, Callable
from underworld.modules.ui.base import UIModule


class UIProgram:
    """Chương trình Giao diện Đồ họa (UI Program) động."""

    def __init__(
        self,
        ui_modules: List[UIModule],
        title: str = "Underworld v0 — World Graphics UI Program"
    ):
        """Khởi tạo UIProgram.

        Args:
            ui_modules: Danh sách các UI Modules đã được lọc và sắp xếp.
            title: Tiêu đề cửa sổ giao diện.
        """
        self.ui_modules = ui_modules
        self.title = title
        self.root: Optional[tk.Tk] = None
        self.main_container: Optional[ttk.Frame] = None
        self.rendered_widgets: List[Any] = []

    def build_gui(
        self,
        initial_state: Dict[str, Any],
        callbacks: Optional[Dict[str, Callable]] = None,
        master: Optional[tk.Tk] = None
    ) -> tk.Tk:
        """Dựng cửa sổ Tkinter và render toàn bộ UI Modules theo đúng thứ tự.

        Args:
            initial_state: Snapshot trạng thái thế giới ban đầu.
            callbacks: Các hàm callback điều khiển từ bên ngoài.
            master: Tkinter root đã có sẵn (nếu có).

        Returns:
            Cửa sổ Tkinter root.
        """
        if master is not None:
            self.root = master
        else:
            self.root = tk.Tk()
            self.root.title(self.title)
            self.root.geometry("900x700")

        # Container chính cuộn được hoặc sắp xếp theo chiều dọc
        self.main_container = ttk.Frame(self.root, padding=10)
        self.main_container.pack(fill="both", expand=True)

        self.refresh_widgets(initial_state, callbacks)
        return self.root

    def refresh_widgets(
        self,
        world_state: Dict[str, Any],
        callbacks: Optional[Dict[str, Callable]] = None
    ) -> None:
        """Làm mới toàn bộ các UI Modules với trạng thái thế giới mới."""
        if self.main_container is None:
            return

        for widget in self.rendered_widgets:
            widget.destroy()
        self.rendered_widgets.clear()

        # Render từng UI Module theo thứ tự đã sắp xếp
        for ui_mod in self.ui_modules:
            try:
                widget = ui_mod.render_tk(self.main_container, world_state, callbacks)
                if widget is not None:
                    widget.pack(fill="x", expand=False, pady=5)
                    self.rendered_widgets.append(widget)
            except Exception as e:
                # Tránh làm hỏng toàn bộ GUI nếu một module gặp lỗi
                err_frame = ttk.LabelFrame(self.main_container, text=f"Lỗi Module {ui_mod.module_id}")
                err_label = ttk.Label(err_frame, text=f"Không thể render: {str(e)}", foreground="red")
                err_label.pack(padx=5, pady=5)
                err_frame.pack(fill="x", pady=5)
                self.rendered_widgets.append(err_frame)
