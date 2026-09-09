"""WorldGraphics — Bộ tổng hợp Giao diện Web UI từ Hệ sinh thái Modules.

WorldGraphics nhận danh sách Modules, lọc ra các UI Modules thích hợp, sắp xếp
layout theo cấu hình và tổng hợp thành một `UIProgram` phục vụ Web UI.
"""

from typing import List, Any, Optional
from underworld.modules.ui.base import UIModule
from underworld.graphics.ui_program import UIProgram


class WorldGraphics:
    """Cơ chế Lọc -> Sắp xếp -> Tổng hợp UI Modules thành UIProgram."""

    def __init__(self, available_modules: Optional[List[Any]] = None):
        """Khởi tạo WorldGraphics.

        Args:
            available_modules: Danh sách toàn bộ Modules có sẵn trong hệ thống.
        """
        self.available_modules = available_modules or []

    def register_module(self, module: Any) -> None:
        """Đăng ký thêm Module vào hệ sinh thái có sẵn."""
        self.available_modules.append(module)

    def filter_ui_modules(self, modules: List[Any]) -> List[UIModule]:
        """Bước 1: Lọc (Filter) ra các Module có khả năng làm UI Module."""
        ui_mods = []
        for mod in modules:
            if isinstance(mod, UIModule) or getattr(mod, "is_ui_module", False):
                ui_mods.append(mod)
        return ui_mods

    def order_ui_modules(
        self,
        ui_modules: List[UIModule],
        layout_order: Optional[List[str]] = None
    ) -> List[UIModule]:
        """Bước 2: Sắp xếp (Order) các UI Modules theo trình tự mong muốn."""
        if not layout_order:
            return ui_modules

        mod_map = {mod.module_id: mod for mod in ui_modules}
        ordered = []

        for mod_id in layout_order:
            if mod_id in mod_map:
                ordered.append(mod_map[mod_id])

        for mod in ui_modules:
            if mod not in ordered:
                ordered.append(mod)

        return ordered

    def compose_ui_program(
        self,
        layout_order: Optional[List[str]] = None,
        title: str = "Underworld v0 — World Graphics Web UI Program"
    ) -> UIProgram:
        """Bước 3 & 4: Tổng hợp (Compose) thành UIProgram hoàn chỉnh.

        Quy trình 4 bước chính xác:
          All Modules -> Filter UI Modules -> Order UI Modules -> Compose UI Program

        Args:
            layout_order: Trật tự ưu tiên các UI Module ID.
            title: Tiêu đề giao diện.

        Returns:
            Thể hiện `UIProgram` đại diện cho chương trình giao diện.
        """
        filtered = self.filter_ui_modules(self.available_modules)
        ordered = self.order_ui_modules(filtered, layout_order=layout_order)
        return UIProgram(ui_modules=ordered, title=title)
