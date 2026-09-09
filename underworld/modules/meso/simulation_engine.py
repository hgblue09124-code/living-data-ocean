"""
Meso Module: SimulationEngineMeso (Thuộc gói underworld.modules.meso).
Meso Module được tổng hợp từ các Atomic Modules nhỏ hơn nhưng là một Module chính thức nằm trong Modules.
"""

from typing import Optional, Callable, List, Dict, Any
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


class SimulationEngineMeso:
    """
    SimulationEngineMeso là một Meso Module (Module tầm trung) nằm trong gói Modules (Modules/meso/).
    Được hợp thành từ 5 Atomic Modules đính kèm:
    - CommandIntakeModule
    - ObservationBuilderModule
    - ActionResolverModule
    - StopPolicyModule
    - TrajectoryRecorderModule

    Hợp đồng (Contract):
    - Input: world, steps, administrator, commands, command_queue, agent_callback, session_controller
    - Output: Trajectory
    """

    def __init__(self, world: Optional[Any] = None):
        """Khởi tạo Meso Module SimulationEngineMeso."""
        self.world = world
        self.command_intake = CommandIntakeModule()
        self.observation_builder = ObservationBuilderModule()
        self.action_resolver = ActionResolverModule()
        self.stop_policy = StopPolicyModule()
        self.trajectory_recorder = TrajectoryRecorderModule()

    def execute(
        self,
        steps: Optional[int] = None,
        administrator: Optional[Administrator] = None,
        commands: Optional[List[AdministratorCommand]] = None,
        command_queue: Optional[Any] = None,
        agent_callback: Optional[Callable[[Observation], Optional[List[Action]]]] = None,
        trajectory_id: str = "traj_meso_001"
    ) -> Trajectory:
        """
        Thực thi mô phỏng qua Meso Module.
        """
        if self.world is None:
            raise ValueError("SimulationEngineMeso yêu cầu phải gán đối tượng World trước khi execute()")

        trajectory = Trajectory(trajectory_id=trajectory_id)
        current_step_count = 0

        while True:
            if self.stop_policy.should_stop([], current_step=current_step_count, max_steps=steps):
                break

            state_before = self.world.get_state()

            active_cmds = self.command_intake.collect_commands(
                administrator=administrator,
                commands=commands,
                command_queue=command_queue,
                world_state=state_before
            )
            commands = None

            if self.stop_policy.should_stop(active_cmds, current_step=current_step_count, max_steps=None):
                break

            for cmd in active_cmds:
                self.world.apply_command(cmd)

            observation = self.observation_builder.build_observation(state_before)

            external_actions, actions_payload = self.action_resolver.resolve_agent_actions(
                observation=observation,
                agent_callback=agent_callback
            )

            state_after = self.world.tick(actions_payload)

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

    def execute_session(
        self,
        session_controller: Optional[Callable[[Any], Dict[str, Any]]] = None,
        administrator: Optional[Administrator] = None,
        agent_callback: Optional[Callable[[Observation], Optional[List[Action]]]] = None,
        trajectory_id: str = "traj_meso_session_001"
    ) -> Trajectory:
        """
        Thực thi phiên mô phỏng tương tác đa giai đoạn qua Meso Module.
        """
        if self.world is None:
            raise ValueError("SimulationEngineMeso yêu cầu phải gán đối tượng World trước khi execute_session()")

        trajectory = Trajectory(trajectory_id=trajectory_id)
        ticks_remaining: Optional[int] = None

        while True:
            state_before = self.world.get_state()

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

            active_cmds = self.command_intake.collect_commands(administrator=administrator)

            if self.stop_policy.should_stop(active_cmds, current_step=0, max_steps=None):
                break

            for cmd in active_cmds:
                self.world.apply_command(cmd)

            observation = self.observation_builder.build_observation(state_before)

            external_actions, actions_payload = self.action_resolver.resolve_agent_actions(
                observation=observation,
                agent_callback=agent_callback
            )

            state_after = self.world.tick(actions_payload)

            self.trajectory_recorder.record_step(
                trajectory=trajectory,
                step=self.world.time_step,
                state_before=state_before,
                observation=observation,
                action=external_actions,
                state_after=state_after
            )

            if ticks_remaining is not None:
                ticks_remaining -= 1

        return trajectory
