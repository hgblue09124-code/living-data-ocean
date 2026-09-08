"""
Định nghĩa Event Loop - Động cơ tự chạy làm cho thế giới Underworld sống.
"""

from typing import Optional, Callable, List
from underworld.world.world import World
from underworld.interface.observation import Observation
from underworld.interface.action import Action
from underworld.data.trajectory import Trajectory


class EventLoop:
    """
    Event Loop đóng vai trò là động cơ chính làm Underworld tự vận hành.

    Quy trình trong mỗi vòng lặp tick:
    1. Lấy trạng thái hiện tại state_t.
    2. Tạo Observation từ state_t.
    3. Nhận danh sách Action từ External Agent (nếu có callback).
    4. Cập nhật WorldState(t+1) bằng `world.tick(actions)`.
    5. Ghi nhận chuỗi chuyển trạng thái vào Trajectory.

    Quan trọng:
    Nếu không có External Agent (agent_callback=None), Event Loop vẫn tự chạy
    mượt mà dựa vào động cơ nội tại của các Human bên trong World.
    """

    def __init__(self, world: World):
        """Khởi tạo Event Loop với một thế giới World."""
        self.world = world

    def run(
        self,
        steps: int,
        trajectory_id: str = "traj_001",
        agent_callback: Optional[Callable[[Observation], Optional[List[Action]]]] = None
    ) -> Trajectory:
        """
        Chạy vòng lặp mô phỏng trong N bước (steps).

        Args:
            steps (int): Số lượng bước (tick) mô phỏng cần chạy.
            trajectory_id (str): Mã định danh cho Trajectory thu được.
            agent_callback (Optional[Callable]): Callback đại diện cho External Agent.
                Nhận vào Observation(t) và trả về danh sách Action(t) tác động vào lượt tiếp theo.

        Returns:
            Trajectory: Chuỗi lịch sử mô phỏng đã được ghi lại đầy đủ.
        """
        trajectory = Trajectory(trajectory_id=trajectory_id)

        for _ in range(steps):
            # 1. Lấy trạng thái hiện tại state_t
            state_before = self.world.get_state()

            # 2. Tạo Observation từ state_t cho Agent bên ngoài
            observation = Observation.from_world_state(state_before)

            # 3. Cho External Agent cơ hội gửi Action tác động (nếu có)
            external_actions: Optional[List[Action]] = None
            if agent_callback is not None:
                external_actions = agent_callback(observation)

            # Convert Action objects to dict for World execution
            actions_payload = (
                [act.to_dict() for act in external_actions]
                if external_actions else None
            )

            # 4. Tiến hành tick chuyển trạng thái sang state_t+1
            state_after = self.world.tick(actions_payload)

            # 5. Ghi bước vừa diễn ra vào Trajectory
            trajectory.add_step(
                step=state_before.time_step + 1,
                state_before=state_before,
                observation=observation,
                action=external_actions,
                state_after=state_after
            )

        return trajectory
