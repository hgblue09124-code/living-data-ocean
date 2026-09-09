"""UIProgram — Chương trình Giao diện Web UI được tổng hợp từ UI Modules.

UIProgram nhận danh sách UI Modules đã được lọc và sắp xếp từ WorldGraphics,
sau đó xuất dữ liệu Web Presentation (Payload JSON/HTML) cho trình duyệt di động/browser.
"""

from typing import List, Dict, Any, Optional
from underworld.modules.ui.base import UIModule


class UIProgram:
    """Chương trình Giao diện Web UI (UI Program) động."""

    def __init__(
        self,
        ui_modules: List[UIModule],
        title: str = "Underworld v0 — World Graphics Web UI Program"
    ):
        """Khởi tạo UIProgram.

        Args:
            ui_modules: Danh sách các UI Modules đã được lọc và sắp xếp.
            title: Tiêu đề giao diện Web.
        """
        self.ui_modules = ui_modules
        self.title = title

    def generate_web_presentation(self, world_state: Dict[str, Any]) -> Dict[str, Any]:
        """Tổng hợp toàn bộ UI Modules thành Web Presentation Payload.

        Args:
            world_state: Snapshot trạng thái thế giới (dict).

        Returns:
            Cấu trúc JSON mô tả toàn bộ giao diện cho Web UI Layer rendering.
        """
        rendered_modules = []
        for mod in self.ui_modules:
            try:
                mod_data = mod.render_web_dict(world_state)
                rendered_modules.append(mod_data)
            except Exception as e:
                rendered_modules.append({
                    "module_id": getattr(mod, "module_id", "unknown"),
                    "title": getattr(mod, "title", "Lỗi UI Module"),
                    "category": "error",
                    "type": "error",
                    "data": {"message": f"Không thể render web dict: {str(e)}"}
                })

        return {
            "title": self.title,
            "time_step": world_state.get("time_step", 0),
            "modules_count": len(rendered_modules),
            "modules": rendered_modules
        }
