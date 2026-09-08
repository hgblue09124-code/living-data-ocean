"""
Định nghĩa trạng thái của thực thể Human trong Underworld.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Any, Optional


@dataclass
class HumanState:
    """
    Lưu trữ toàn bộ trạng thái nội tại của một Human tại một thời điểm t.

    Attributes:
        id (str): Mã định danh duy nhất của Human.
        position (Tuple[int, int]): Vị trí hiện tại trong không gian (x, y).
        status (str): Trạng thái hiện tại (ví dụ: 'nghỉ_ngơi', 'di_chuyển', 'tìm_kiếm').
        needs (Dict[str, float]): Các chỉ số nhu cầu cơ bản (năng lượng, đói, xã hội...).
        goals (List[str]): Danh sách mục tiêu hiện tại.
        memory (List[Dict[str, Any]]): Ký ức ngắn hạn / lịch sử sự kiện đã ghi nhớ.
        action_history (List[str]): Lịch sử các hành động đã thực hiện.
    """
    id: str
    position: Tuple[int, int] = (0, 0)
    status: str = "nghỉ_ngơi"
    needs: Dict[str, float] = field(default_factory=lambda: {
        "năng_lượng": 100.0,
        "đói": 0.0,
        "xã_hội": 50.0
    })
    goals: List[str] = field(default_factory=lambda: ["khám_phá"])
    memory: List[Dict[str, Any]] = field(default_factory=list)
    action_history: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Chuyển đổi trạng thái Human thành dict để serialization."""
        return {
            "id": self.id,
            "position": list(self.position),
            "status": self.status,
            "needs": dict(self.needs),
            "goals": list(self.goals),
            "memory": list(self.memory),
            "action_history": list(self.action_history),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "HumanState":
        """Khôi phục trạng thái Human từ dict."""
        return cls(
            id=data["id"],
            position=tuple(data.get("position", (0, 0))),
            status=data.get("status", "nghỉ_ngơi"),
            needs=data.get("needs", {"năng_lượng": 100.0, "đói": 0.0, "xã_hội": 50.0}),
            goals=data.get("goals", ["khám_phá"]),
            memory=data.get("memory", []),
            action_history=data.get("action_history", [])
        )
