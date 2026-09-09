"""
Mô-đun Runtime chứa EventLoop điều phối vòng lặp mô phỏng Underworld.
"""

from typing import Optional, Callable, List, Dict, Any
from underworld.composition.world import World
from underworld.interface.observation import Observation
from underworld.interface.action import Action
from underworld.interface.command import AdministratorCommand
from underworld.interface.administrator import Administrator
from underworld.data.trajectory import Trajectory


class EventLoop:
    """
    Event Loop đóng vai trò là Runtime điều phối mô phỏng.

    Ranh giới kiến trúc:
    - World là Composition root của simulation, tự vận hành hoàn toàn độc lập.
    - Administrator là giao diện điều khiển bên ngoài gửi `AdministratorCommand`.
    - External Agent nhận `Observation` và trả về `Action`.
    - Runtime nhận các lệnh/tác động và chuyển sang cho `World`.
    """

    def __init__(self, world: World):
        """Khởi tạo Event Loop với một thế giới World."""
        self.world = world

    def run(
        self,
        steps: Optional[int] = None,
        administrator: Optional[Administrator] = None,
        commands: Optional[List[AdministratorCommand]] = None,
        command_queue: Optional[Any] = None,
        agent_callback: Optional[Callable[[Observation], Optional[List[Action]]]] = None,
        trajectory_id: str = "traj_001"
    ) -> Trajectory:
        """
        Chạy vòng lặp mô phỏng.

        Args:
            steps (Optional[int]): Số bước mô phỏng tối đa. Nếu là None, thế giới
                sẽ chạy liên tục cho đến khi nhận được lệnh REQUEST_STOP từ bên ngoài.
            administrator (Optional[Administrator]): Giao diện điều khiển từ bên ngoài.
            commands (Optional[List[AdministratorCommand]]): Danh sách lệnh trực tiếp từ bên ngoài.
            command_queue (Optional[Any]): Hàng chờ lệnh hoặc callback trả về lệnh động.
            agent_callback (Optional[Callable]): Callback đại diện cho External Agent.
            trajectory_id (str): Mã định danh cho Trajectory.

        Returns:
            Trajectory: Chuỗi lịch sử mô phỏng đã ghi nhận.
        """
        trajectory = Trajectory(trajectory_id=trajectory_id)
        current_step_count = 0

        while True:
            # Kiểm tra giới hạn số bước
            if steps is not None and current_step_count >= steps:
                break

            # 1. Lấy trạng thái hiện tại trước tick
            state_before = self.world.get_state()

            # 2. Thu thập các lệnh AdministratorCommand từ bên ngoài
            active_commands: List[AdministratorCommand] = []
            if commands:
                active_commands.extend(commands)
                commands = None  # Xóa danh sách lệnh tĩnh sau khi nhận ở lượt đầu

            if administrator is not None:
                active_commands.extend(administrator.get_pending_commands())

            if command_queue is not None:
                if callable(command_queue):
                    q_cmds = command_queue(state_before)
                    if q_cmds:
                        active_commands.extend(q_cmds)
                elif hasattr(command_queue, "get_pending_commands"):
                    active_commands.extend(command_queue.get_pending_commands())
                elif hasattr(command_queue, "pop") or hasattr(command_queue, "get"):
                    while hasattr(command_queue, "__len__") and len(command_queue) > 0:
                        active_commands.append(command_queue.pop(0))

            # 3. Áp dụng các lệnh từ bên ngoài và kiểm tra lệnh REQUEST_STOP
            stop_requested = False
            for cmd in active_commands:
                cmd_type = getattr(cmd, "command_type", None) or (cmd.get("command_type") if isinstance(cmd, dict) else None)
                if cmd_type == "REQUEST_STOP":
                    stop_requested = True
                else:
                    self.world.apply_command(cmd)

            if stop_requested:
                break

            # 4. Tạo Observation từ state_before cho External Agent
            observation = Observation.from_world_state(state_before)

            # 5. Tiếp nhận Action từ External Agent (nếu có)
            external_actions: Optional[List[Action]] = None
            if agent_callback is not None:
                external_actions = agent_callback(observation)

            actions_payload = (
                [act.to_dict() for act in external_actions]
                if external_actions else None
            )

            # 6. Tiến hành tick chuyển trạng thái sang state_after
            state_after = self.world.tick(actions_payload)

            # 7. Ghi bước vừa diễn ra vào Trajectory
            current_step_count += 1
            trajectory.add_step(
                step=self.world.time_step,
                state_before=state_before,
                observation=observation,
                action=external_actions,
                state_after=state_after
            )

        return trajectory

    def run_session(
        self,
        session_controller: Optional[Callable[[Any], Dict[str, Any]]] = None,
        administrator: Optional[Administrator] = None,
        agent_callback: Optional[Callable[[Observation], Optional[List[Action]]]] = None,
        trajectory_id: str = "traj_session_001"
    ) -> Trajectory:
        """
        Khởi chạy phiên mô phỏng tương tác Control Loop đa giai đoạn.

        Phương thức này cho phép Administrator / Session Controller nhận quyền điều khiển
        sau mỗi giai đoạn với các lựa chọn:
        - {"action": "CONTINUE"}: Mô phỏng tiếp tục tự động.
        - {"action": "RUN_N_TICKS", "ticks": N}: Chạy đúng N ticks rồi trả lại quyền quan sát/điều khiển.
        - {"action": "COMMAND", "commands": [...]}: Nạp danh sách AdministratorCommand.
        - {"action": "OBSERVE"}: Quan sát trạng thái snapshot hiện tại.
        - {"action": "STOP"}: Dừng phiên mô phỏng hoàn toàn.
        """
        trajectory = Trajectory(trajectory_id=trajectory_id)
        ticks_remaining: Optional[int] = None

        while True:
            state_before = self.world.get_state()

            # Gọi Session Controller ở đầu giai đoạn nếu cần can thiệp
            if session_controller is not None and (ticks_remaining is None or ticks_remaining <= 0):
                ctrl_response = session_controller(state_before) or {}
                act = str(ctrl_response.get("action", "CONTINUE")).upper()

                if act == "STOP":
                    break
                elif act == "RUN_N_TICKS":
                    ticks_remaining = int(ctrl_response.get("ticks", 1))
                elif act == "COMMAND":
                    cmds = ctrl_response.get("commands", [])
                    if administrator:
                        for c in cmds:
                            if isinstance(c, AdministratorCommand):
                                administrator._pending_commands.append(c)
                            elif isinstance(c, dict):
                                administrator._pending_commands.append(AdministratorCommand.from_dict(c))
                    else:
                        for c in cmds:
                            if isinstance(c, AdministratorCommand):
                                self.world.apply_command(c)
                            elif isinstance(c, dict):
                                self.world.apply_command(AdministratorCommand.from_dict(c))
                elif act == "CONTINUE":
                    ticks_remaining = None

            # Thu thập lệnh từ Administrator
            active_commands: List[AdministratorCommand] = []
            if administrator is not None:
                active_commands.extend(administrator.get_pending_commands())

            stop_requested = False
            for cmd in active_commands:
                cmd_type = getattr(cmd, "command_type", None) or (cmd.get("command_type") if isinstance(cmd, dict) else None)
                if cmd_type == "REQUEST_STOP":
                    stop_requested = True
                else:
                    self.world.apply_command(cmd)

            if stop_requested:
                break

            # External Agent interaction
            observation = Observation.from_world_state(state_before)
            external_actions: Optional[List[Action]] = None
            if agent_callback is not None:
                external_actions = agent_callback(observation)

            actions_payload = (
                [act.to_dict() for act in external_actions]
                if external_actions else None
            )

            # Execution tick
            state_after = self.world.tick(actions_payload)

            trajectory.add_step(
                step=self.world.time_step,
                state_before=state_before,
                observation=observation,
                action=external_actions,
                state_after=state_after
            )

            if ticks_remaining is not None:
                ticks_remaining -= 1

        return trajectory

    def chay(
        self,
        so_buoc: Optional[int] = None,
        quan_tri_vien: Optional[Any] = None,
        agent_callback: Optional[Callable[[Observation], Optional[List[Action]]]] = None,
        trajectory_id: str = "traj_001"
    ) -> Trajectory:
        """Phương thức bí danh (alias) tiếng Việt tương thích với cấu hình cũ."""
        return self.run(
            steps=so_buoc,
            administrator=quan_tri_vien,
            agent_callback=agent_callback,
            trajectory_id=trajectory_id
        )
