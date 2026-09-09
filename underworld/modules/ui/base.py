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

    def render_tk(
        self,
        parent_widget: Any,
        world_state: Dict[str, Any],
        callbacks: Optional[Dict[str, Callable]] = None
    ) -> Any:
        """Dựng giao diện Tkinter cho module này.

        Args:
            parent_widget: Widget Tkinter cha chứa phần tử UI này.
            world_state: Snapshot trạng thái thế giới hiện tại.
            callbacks: Các hàm callback điều khiển từ bên ngoài (ví dụ: on_step, on_command).

        Returns:
            Widget Tkinter đại diện cho giao diện của module.
        """
        raise NotImplementedError("Các UI Module con phải cài đặt phương thức render_tk()")
