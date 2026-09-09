"""
Mô-đun Atomic quản lý thuộc tính nhu cầu sinh học và ký ức thực thể (EntityNeeds).
"""

import copy
from typing import Dict, List, Any, Optional


class EntityNeeds:
    """
    Quản lý các chỉ số sinh học (năng lượng, đói, xã hội), trạng thái, mục tiêu và ký ức.
    """

    def __init__(
        self,
        status: str = "thong_dong",
        needs: Optional[Dict[str, float]] = None,
        goals: Optional[List[str]] = None
    ):
        """Khởi tạo trạng thái nội tại thực thể."""
        self.status = status
        self.needs = needs if needs is not None else {
            "năng_lượng": 100.0,
            "đói": 0.0,
            "xã_hội": 50.0
        }
        self.goals = goals if goals is not None else ["khám_phá"]
        self.memory: List[Dict[str, Any]] = []
        self.action_history: List[str] = []

    def update_biology(self) -> None:
        """Cập nhật các biến đổi sinh học qua mỗi tick."""
        self.needs["năng_lượng"] = max(0.0, self.needs["năng_lượng"] - 2.0)
        self.needs["đói"] = min(100.0, self.needs["đói"] + 3.0)
        self.needs["xã_hội"] = max(0.0, self.needs["xã_hội"] - 1.0)

    def record_action(self, action_name: str, position: tuple) -> None:
        """Ghi nhận lịch sử hành động và ký ức ngắn hạn."""
        self.action_history.append(action_name)
        self.memory.append({
            "hành_động": action_name,
            "vị_trí": position,
            "trạng_thái": self.status
        })
        if len(self.memory) > 20:
            self.memory.pop(0)

    def to_dict(self) -> Dict[str, Any]:
        """Xuất thuộc tính nhu cầu dạng dict độc lập."""
        return {
            "status": self.status,
            "needs": copy.deepcopy(self.needs),
            "goals": list(self.goals),
            "memory": copy.deepcopy(self.memory),
            "action_history": list(self.action_history)
        }
