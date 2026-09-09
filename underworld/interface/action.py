"""
Định nghĩa đối tượng Action - Tác động từ External Agent gửi vào Underworld.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class Action:
    """
    Hành động tác động từ Agent bên ngoài vào Underworld.

    Agent bên ngoài chỉ có thể tác động vào thế giới thông qua đối tượng Action này,
    không được sửa trực tiếp trạng thái nội tại của World hay Human.

    Attributes:
        action_type (str): Loạt tác động (ví dụ: 'MOVE', 'REST', 'SET_GOAL').
        target_id (Optional[str]): Mã Human mục tiêu chịu tác động.
        payload (Dict[str, Any]): Tham số chi tiết đi kèm hành động.
    """
    action_type: str
    target_id: Optional[str] = None
    payload: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Chuyển đổi Action thành dict để serialization/ghi trajectory."""
        return {
            "action_type": self.action_type,
            "target_id": self.target_id,
            "payload": self.payload
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Action":
        """Khôi phục Action từ dict."""
        return cls(
            action_type=data.get("action_type", "UNKNOWN"),
            target_id=data.get("target_id"),
            payload=data.get("payload", {})
        )
