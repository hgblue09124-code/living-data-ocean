"""
Administrator - Interface điều khiển bên ngoài cho Quản trị viên (External Human Control Interface).
"""

from typing import List, Dict, Any, Optional
from underworld.interface.command import AdministratorCommand


class Administrator:
    """
    Administrator đại diện cho giao diện điều khiển của con người từ bên ngoài (External Human Control Interface).

    Lưu ý kiến trúc quan trọng:
    - Administrator KHÔNG phải là Agent hay actor bên trong World.
    - World KHÔNG phụ thuộc vào Administrator để tự vận hành.
    - Administrator tạo ra các `AdministratorCommand` để Runtime/World tiếp nhận và xử lý.
    """

    def __init__(self, name: str = "SystemAdministrator"):
        """Khởi tạo Administrator."""
        self.name = name
        self._pending_commands: List[AdministratorCommand] = []

    def change_environment(self, key: str, val: Any) -> AdministratorCommand:
        """Tạo lệnh thay đổi biến môi trường."""
        cmd = AdministratorCommand(
            command_type="CHANGE_ENVIRONMENT",
            payload={"key": key, "val": val}
        )
        self._pending_commands.append(cmd)
        return cmd

    def create_event(self, detail: str) -> AdministratorCommand:
        """Tạo lệnh phát sinh sự kiện ngoài thế giới."""
        cmd = AdministratorCommand(
            command_type="CREATE_EVENT",
            payload={"detail": detail}
        )
        self._pending_commands.append(cmd)
        return cmd

    def affect_human(
        self,
        human_id: str,
        action_type: str,
        payload: Optional[Dict[str, Any]] = None
    ) -> AdministratorCommand:
        """Tạo lệnh tác động đến một Human cụ thể."""
        cmd = AdministratorCommand(
            command_type="AFFECT_HUMAN",
            target_id=human_id,
            payload={"action_type": action_type, "payload": payload or {}}
        )
        self._pending_commands.append(cmd)
        return cmd

    def request_stop(self) -> AdministratorCommand:
        """Tạo lệnh yêu cầu dừng mô phỏng thế giới."""
        cmd = AdministratorCommand(command_type="REQUEST_STOP")
        self._pending_commands.append(cmd)
        return cmd

    def get_pending_commands(self) -> List[AdministratorCommand]:
        """Lấy danh sách các lệnh đang chờ và làm sạch hàng chờ."""
        cmds = list(self._pending_commands)
        self._pending_commands.clear()
        return cmds
