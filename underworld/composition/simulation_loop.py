"""
Mô-đun Composition hợp thành vòng lặp mô phỏng từ các Atomic Modules.
"""

from typing import Optional, Callable, List, Dict, Any
from underworld.composition.world import World
from underworld.composition.state import WorldState
from underworld.interface.observation import Observation
from underworld.interface.action import Action
from underworld.interface.command import AdministratorCommand
from underworld.interface.administrator import Administrator
from underworld.data.trajectory import Trajectory

from underworld.modules.command_intake import CommandIntakeModule
from underworld.modules.observation_builder import ObservationBuilderModule
from underworld.modules.action_resolver import ActionResolverModule
from underworld.modules.stop_policy import StopPolicyModule
from underworld.modules.trajectory_recorder import TrajectoryRecorderModule


class SimulationLoopComposition:
    """
    Composition tổng hợp các Atomic Modules:
    - CommandIntakeModule: Thu thập lệnh
    - ObservationBuilderModule: Dựng quan sát
    - ActionResolverModule: Xử lý tác động agent
    - StopPolicyModule: Đánh giá điều kiện dừng
    - TrajectoryRecorderModule: Ghi nhận lịch sử
    """

    def __init__(self, world: World):
        """Khởi tạo Composition của vòng lặp mô phỏng."""
        self.world = world
        self.command_intake = CommandIntakeModule()
        self.observation_builder = ObservationBuilderModule()
        self.action_resolver = ActionResolverModule()
        self.stop_policy = StopPolicyModule()
        self.trajectory_recorder = TrajectoryRecorderModule()

    def run_steps(
        self,
        steps: Optional[int] = None,
        administrator: Optional[Administrator] = None,
        commands: Optional[List[AdministratorCommand]] = None,
        command_queue: Optional[Any] = None,
        agent_callback: Optional[Callable[[Observation], Optional[List[Action]]]] = None,
        trajectory_id: str = "traj_comp_001"
    ) -> Trajectory:
        """
        Thực thi các bước mô phỏng thông qua phối hợp các Atomic Modules.
        """
        trajectory = Trajectory(trajectory_id=trajectory_id)
        current_step_count = 0

        while True:
            # 1. Đánh giá dừng trước tick theo giới hạn số bước
            if self.stop_policy.should_stop([], current_step=current_step_count, max_steps=steps):
                break

            # 2. Lấy trạng thái hiện tại
            state_before = self.world.get_state()

            # 3. Thu thập các AdministratorCommand từ bên ngoài
            active_cmds = self.command_intake.collect_commands(
                administrator=administrator,
                commands=commands,
                command_queue=command_queue,
                world_state=state_before
            )
            commands = None  # Clear static commands after first intake

            # 4. Đánh giá lệnh REQUEST_STOP và áp dụng các lệnh quản trị
            if self.stop_policy.should_stop(active_cmds, current_step=current_step_count, max_steps=None):
                break

            for cmd in active_cmds:
                self.world.apply_command(cmd)

            # 5. Dựng Observation cho External Agent
            observation = self.observation_builder.build_observation(state_before)

            # 6. Tiếp nhận Action từ External Agent
            external_actions, actions_payload = self.action_resolver.resolve_agent_actions(
                observation=observation,
                agent_callback=agent_callback
            )

            # 7. Tiến hành tick World
            state_after = self.world.tick(actions_payload)

            # 8. Ghi nhận TrajectoryStep
            current_step_count += 1
            self.trajectory_recorder.record_step(
                trajectory=trajectory,
                step=self.world.time_step,
                state_before=state_before,
                observation=observation,
                action=external_actions,
                state_after=state_after
            )

        return trajectory
