"""
Mô-đun Runtime chứa EventLoop điều phối vòng lặp mô phỏng Underworld.
EventLoop ủy quyền thực thi vòng lặp cho Meso Module (SimulationEngineMeso).
"""

from typing import Optional, Callable, List, Dict, Any
from underworld.composition.world import World
from underworld.interface.observation import Observation
from underworld.interface.action import Action
from underworld.interface.command import AdministratorCommand
from underworld.interface.administrator import Administrator
from underworld.data.trajectory import Trajectory
from underworld.modules.meso.simulation_engine import SimulationEngineMeso


class EventLoop:
    """
    Event Loop đóng vai trò là Runtime điều phối mô phỏng.

    Ranh giới kiến trúc:
    - World là Composition root của simulation, tự vận hành hoàn toàn độc lập.
    - EventLoop sử dụng Meso Module (SimulationEngineMeso) để thực thi vòng lặp mô phỏng.
    - Administrator là giao diện điều khiển bên ngoài gửi `AdministratorCommand`.
    - External Agent nhận `Observation` và trả về `Action`.
    """

    def __init__(self, world: World):
        """Khởi tạo Event Loop với một thế giới World."""
        self.world = world
        self.engine_meso = SimulationEngineMeso(world)

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
        Chạy vòng lặp mô phỏng bằng cách ủy quyền cho Meso Module SimulationEngineMeso.
        """
        return self.engine_meso.execute(
            steps=steps,
            administrator=administrator,
            commands=commands,
            command_queue=command_queue,
            agent_callback=agent_callback,
            trajectory_id=trajectory_id
        )

    def run_session(
        self,
        session_controller: Optional[Callable[[Any], Dict[str, Any]]] = None,
        administrator: Optional[Administrator] = None,
        agent_callback: Optional[Callable[[Observation], Optional[List[Action]]]] = None,
        trajectory_id: str = "traj_session_001"
    ) -> Trajectory:
        """
        Khởi chạy phiên mô phỏng tương tác Control Loop đa giai đoạn thông qua Meso Module.
        """
        return self.engine_meso.execute_session(
            session_controller=session_controller,
            administrator=administrator,
            agent_callback=agent_callback,
            trajectory_id=trajectory_id
        )

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
