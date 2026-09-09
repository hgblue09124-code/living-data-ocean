"""
Mô-đun Kernel quản lý thời gian mô phỏng (SimulationTime).
"""

from dataclasses import dataclass


@dataclass
class SimulationTime:
    """
    Quản lý thời gian t của thế giới mô phỏng.
    """
    time_step: int = 0

    def increment(self) -> int:
        """Tăng time_step thêm 1 đơn vị."""
        self.time_step += 1
        return self.time_step

    def reset(self) -> None:
        """Đặt lại time_step về 0."""
        self.time_step = 0
