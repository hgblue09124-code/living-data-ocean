"""
Mô-đun Atomic tiếp nhận lệnh từ Administrator / Command Queue (CommandIntakeModule).
"""

from typing import List, Dict, Any, Optional
from underworld.interface.command import AdministratorCommand
from underworld.interface.administrator import Administrator


class CommandIntakeModule:
    """
    Trách nhiệm: Thu thập các AdministratorCommand từ bên ngoài (administrator, command_queue, hoặc static commands list).
    """

    def collect_commands(
        self,
        administrator: Optional[Administrator] = None,
        commands: Optional[List[AdministratorCommand]] = None,
        command_queue: Optional[Any] = None,
        world_state: Optional[Any] = None
    ) -> List[AdministratorCommand]:
        """
        Thu thập tất cả các lệnh AdministratorCommand đang chờ xử lý.
        """
        active_commands: List[AdministratorCommand] = []

        if commands:
            active_commands.extend(commands)

        if administrator is not None:
            active_commands.extend(administrator.get_pending_commands())

        if command_queue is not None:
            if callable(command_queue):
                q_cmds = command_queue(world_state)
                if q_cmds:
                    for cmd in q_cmds:
                        if isinstance(cmd, AdministratorCommand):
                            active_commands.append(cmd)
                        elif isinstance(cmd, dict):
                            active_commands.append(AdministratorCommand.from_dict(cmd))
            elif hasattr(command_queue, "get_pending_commands"):
                active_commands.extend(command_queue.get_pending_commands())
            elif hasattr(command_queue, "pop") or hasattr(command_queue, "get"):
                while hasattr(command_queue, "__len__") and len(command_queue) > 0:
                    c = command_queue.pop(0)
                    if isinstance(c, AdministratorCommand):
                        active_commands.append(c)
                    elif isinstance(c, dict):
                        active_commands.append(AdministratorCommand.from_dict(c))

        return active_commands
