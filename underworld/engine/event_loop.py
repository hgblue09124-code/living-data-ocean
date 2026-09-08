"""
Định nghĩa Event Loop - Động cơ tự chạy làm cho thế giới Underworld sống.
"""

from typing import Optional, Callable, List, Dict, Any
from underworld.world.world import World
from underworld.interface.observation import Observation
from underworld.interface.action import Action
from underworld.interface.quan_tri_vien import QuanTriVien
from underworld.data.trajectory import Trajectory


class EventLoop:
    """
    Event Loop đóng vai trò là động cơ chính làm Underworld tự vận hành.

    Thứ tự xác định ở MỖI bước thời gian:
    1. Lấy trạng thái hiện tại state_t.
    2. Cho Quản trị viên quan sát state_t qua `quan_tri_vien.tai_moi_buoc(state_t)`.
    3. Áp dụng các lệnh tác động từ Quản trị viên vào thế giới.
    4. Cập nhật WorldState(t+1) bằng `world.tick()`.
    5. Tạo Observation(t+1) cho Agent bên ngoài và tiếp nhận Action.
    6. Áp dụng Action từ Agent bên ngoài (nếu có).
    7. Ghi nhận bước chuyển đổi vào Trajectory.
    8. Kiểm tra điều kiện dừng (Quản trị viên yêu cầu dừng hoặc đạt giới hạn so_buoc).

    Đặc biệt:
    - Hỗ trợ chạy liên tục vô hạn khi `so_buoc=None`.
    - Hỗ trợ chạy giới hạn đúng N bước khi `so_buoc=N`.
    """

    def __init__(self, world: World):
        """Khởi tạo Event Loop với một thế giới World."""
        self.world = world

    def chay(
        self,
        so_buoc: Optional[int] = None,
        quan_tri_vien: Optional[QuanTriVien] = None,
        agent_callback: Optional[Callable[[Observation], Optional[List[Action]]]] = None,
        trajectory_id: str = "traj_001"
    ) -> Trajectory:
        """
        Chạy vòng lặp mô phỏng.

        Args:
            so_buoc (Optional[int]): Số bước mô phỏng tối đa. Nếu là None, thế giới
                sẽ chạy liên tục cho đến khi Quản trị viên yêu cầu dừng.
            quan_tri_vien (Optional[QuanTriVien]): Đối tượng Quản trị viên can thiệp ở mọi bước.
            agent_callback (Optional[Callable]): Callback đại diện cho External Agent.
            trajectory_id (str): Mã định danh cho Trajectory.

        Returns:
            Trajectory: Chuỗi lịch sử mô phỏng đã ghi nhận.
        """
        trajectory = Trajectory(trajectory_id=trajectory_id)
        buoc_hien_tai = 0

        while True:
            # Kiểm tra xem đã đạt giới hạn so_buoc hay chưa
            if so_buoc is not None and buoc_hien_tai >= so_buoc:
                break

            # 1. Lấy trạng thái hiện tại trước tick
            state_before = self.world.get_state()

            # 2. Cho Quản trị viên quan sát và đưa ra lệnh điều khiển ở MỖI bước thời gian
            lenh_quan_tri: List[Dict[str, Any]] = []
            if quan_tri_vien is not None:
                lenh_quan_tri = quan_tri_vien.tai_moi_buoc(state_before)
                # Áp dụng tác động quản trị trực tiếp lên thế giới
                quan_tri_vien.ap_dung_tac_dong_quan_tri(self.world, lenh_quan_tri)

                # Kiểm tra ngay nếu Quản trị viên yêu cầu dừng trước tick
                if quan_tri_vien.dang_yeu_cau_dung():
                    break

            # 3. Tạo Observation từ state_before cho External Agent
            observation = Observation.from_world_state(state_before)

            # 4. Cho External Agent cơ hội gửi Action tác động (nếu có)
            external_actions: Optional[List[Action]] = None
            if agent_callback is not None:
                external_actions = agent_callback(observation)

            actions_payload = (
                [act.to_dict() for act in external_actions]
                if external_actions else None
            )

            # 5. Tiến hành tick chuyển trạng thái sang state_after
            state_after = self.world.tick(actions_payload)

            # 6. Ghi bước vừa diễn ra vào Trajectory
            buoc_hien_tai += 1
            trajectory.add_step(
                step=self.world.time_step,
                state_before=state_before,
                observation=observation,
                action=external_actions,
                state_after=state_after
            )

            # 7. Kiểm tra nếu Quản trị viên vừa yêu cầu dừng trong quá trình tick
            if quan_tri_vien is not None and quan_tri_vien.dang_yeu_cau_dung():
                break

        return trajectory

    def run(
        self,
        steps: Optional[int] = None,
        trajectory_id: str = "traj_001",
        agent_callback: Optional[Callable[[Observation], Optional[List[Action]]]] = None,
        quan_tri_vien: Optional[QuanTriVien] = None
    ) -> Trajectory:
        """Phương thức bí danh (alias) tương thích ngược với phiên bản trước."""
        return self.chay(
            so_buoc=steps,
            quan_tri_vien=quan_tri_vien,
            agent_callback=agent_callback,
            trajectory_id=trajectory_id
        )
