"""
Định nghĩa Dataset phục vụ thu thập và xuất tập dữ liệu mô phỏng dạng JSONL.
"""

import json
from typing import List, Dict, Any, Optional
from underworld.data.trajectory import Trajectory


class Dataset:
    """
    Tập dữ liệu Dataset thu gom nhiều Trajectory từ các phiên chạy Underworld.

    Cung cấp khả năng xuất dữ liệu ra tệp dạng JSONL (hoặc nạp vào)
    cực kỳ nhẹ nhàng, không cần đến cơ sở dữ liệu hay thư viện phức tạp.
    """

    def __init__(self):
        """Khởi tạo một tập dữ liệu rỗng."""
        self.trajectories: List[Trajectory] = []

    def add_trajectory(self, trajectory: Trajectory) -> None:
        """Thêm một Trajectory vào Dataset."""
        self.trajectories.append(trajectory)

    def export_jsonl(self, filepath: str) -> None:
        """
        Xuất toàn bộ Dataset thành tệp JSONL.
        Mỗi dòng tương ứng với một Trajectory hoàn chỉnh.
        """
        with open(filepath, "w", encoding="utf-8") as f:
            for traj in self.trajectories:
                f.write(json.dumps(traj.to_dict(), ensure_ascii=False) + "\n")

    @classmethod
    def load_jsonl(cls, filepath: str) -> List[Dict[str, Any]]:
        """
        Nạp dữ liệu từ tệp JSONL.
        Trả về danh sách dữ liệu dict của các Trajectory.
        """
        results = []
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    results.append(json.loads(line.strip()))
        return results
