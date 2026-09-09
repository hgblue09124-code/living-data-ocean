"""
Mô-đun Atomic đánh giá điều kiện dừng mô phỏng (StopPolicyModule).
"""

from typing import List, Any, Optional
from underworld.interface.command import AdministratorCommand


class StopPolicyModule:
    """
    Trách nhiệm: Đánh giá xem có yêu cầu dừng mô phỏng hay không từ danh sách lệnh AdministratorCommand hoặc số bước.
    """

    def should_stop(
        self,
        commands: List[AdministratorCommand],
        current_step: int,
        max_steps: Optional[int] = None
    ) -> bool:
        """
        Kiểm tra xem vòng lặp có nên dừng hay không.
        """
        if max_steps is not None and current_step >= max_steps:
            return True

        for cmd in commands:
            cmd_type = getattr(cmd, "command_type", None) or (cmd.get("command_type") if isinstance(cmd, dict) else None)
            if cmd_type == "REQUEST_STOP":
                return True

        return False
