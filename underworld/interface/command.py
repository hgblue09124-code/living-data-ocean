"""
AdministratorCommand - Trung gian lệnh điều khiển giữa Administrator và World.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, Optional


@dataclass
class AdministratorCommand:
    """
    AdministratorCommand là boundary trung gian giữa Administrator (người dùng bên ngoài)
    và thế giới Underworld.

    Attributes:
        command_type (str): Loại lệnh ('CHANGE_ENVIRONMENT', 'CREATE_EVENT', 'AFFECT_HUMAN', 'REQUEST_STOP').
        payload (Dict[str, Any]): Dữ liệu đi kèm lệnh.
        target_id (Optional[str]): Định danh đối tượng bị tác động (nếu có).
    """
    command_type: str
    payload: Dict[str, Any] = field(default_factory=dict)
    target_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Chuyển đổi AdministratorCommand thành dict để serialization."""
        return {
            "command_type": self.command_type,
            "payload": self.payload,
            "target_id": self.target_id
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AdministratorCommand":
        """Khôi phục AdministratorCommand từ dict."""
        return cls(
            command_type=data.get("command_type", "UNKNOWN"),
            payload=data.get("payload", {}),
            target_id=data.get("target_id")
        )
