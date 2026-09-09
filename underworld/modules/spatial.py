"""
Mô-đun Atomic quản lý không gian và vị trí (SpatialSpace).
"""

import copy
from typing import Tuple, List


class SpatialSpace:
    """
    Quản lý tọa độ không gian (x, y) và khoảng cách giữa các thực thể.
    """

    def __init__(self, bounds: Tuple[int, int] = (100, 100), position: Tuple[int, int] = (0, 0)):
        """Khởi tạo không gian với giới hạn (bounds) và vị trí ban đầu."""
        self.bounds = bounds
        self.position = tuple(position)

    def move_by(self, dx: int, dy: int) -> Tuple[int, int]:
        """Di chuyển vị trí thêm (dx, dy)."""
        new_x = self.position[0] + dx
        new_y = self.position[1] + dy
        self.position = (new_x, new_y)
        return self.position

    def set_position(self, pos: Tuple[int, int]) -> Tuple[int, int]:
        """Đặt vị trí mới."""
        self.position = tuple(pos)
        return self.position

    def manhattan_distance(self, other_position: Tuple[int, int]) -> int:
        """Tính khoảng cách Manhattan đến vị trí khác."""
        return abs(self.position[0] - other_position[0]) + abs(self.position[1] - other_position[1])

    def to_dict(self) -> dict:
        """Xuất thông tin không gian dạng dict."""
        return {
            "bounds": list(self.bounds),
            "position": list(self.position)
        }
