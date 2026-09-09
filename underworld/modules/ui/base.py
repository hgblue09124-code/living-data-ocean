"""Giao diện nền tảng cho các UI Modules trong Underworld.

Mỗi UI Module đại diện cho một thành phần giao diện nguyên tử có khả năng hiển thị
hoặc tương tác với một khía cạnh của thế giới mô phỏng.
"""

from typing import Dict, Any, Optional, Callable


class UIModule:
    """Lớp cơ sở cho mọi UI Module trong hệ sinh thái Underworld."""

    def __init__(self, module_id: str, title: str, category: str = "general"):
        """Khởi tạo UI Module.

        Args:
            module_id: Định danh duy nhất của UI Module.
            title: Tiêu đề hiển thị trên giao diện.
            category: Phân loại module (ví dụ: 'view', 'control', 'timeline').
        """
        self.module_id = module_id
        self.title = title
        self.category = category
        self.is_ui_module = True

    def render_web_dict(self, world_state: Dict[str, Any]) -> Dict[str, Any]:
        """Cung cấp dữ liệu đã cấu trúc hóa dành cho Web UI Presentation Layer.

        Args:
            world_state: Snapshot trạng thái thế giới hiện tại.

        Returns:
            Dict dữ liệu giao diện của module.
        """
        raise NotImplementedError("Các UI Module con phải cài đặt phương thức render_web_dict()")

    def render_tk(
        self,
        parent_widget: Any,
        world_state: Dict[str, Any],
        callbacks: Optional[Dict[str, Callable]] = None
    ) -> Any:
        """Dựng giao diện Tkinter cho module này (nếu có hỗ trợ)."""
        pass
