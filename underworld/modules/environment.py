"""
Mô-đun Atomic quản lý trạng thái môi trường (EnvironmentState).
"""

import copy
from typing import Dict, Any, Tuple


class EnvironmentState:
    """
    Quản lý các thuộc tính môi trường thế giới (thời tiết, tài nguyên).
    """

    def __init__(self, bounds: Tuple[int, int] = (100, 100)):
        """Khởi tạo môi trường."""
        self.bounds = bounds
        self.weather = "bình_thường"
        self.resources = {"thức_ăn": 50, "nước": 50}

    def set_attribute(self, key: str, value: Any) -> None:
        """Cập nhật hoặc thêm một biến môi trường."""
        if key == "weather":
            self.weather = str(value)
        elif key == "bounds" and isinstance(value, (list, tuple)):
            self.bounds = tuple(value)
        else:
            self.resources[key] = value

    def to_dict(self) -> Dict[str, Any]:
        """Xuất thông tin môi trường dạng dict độc lập."""
        return {
            "bounds": list(self.bounds),
            "weather": self.weather,
            "resources": copy.deepcopy(self.resources)
        }
