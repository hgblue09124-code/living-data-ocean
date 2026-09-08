"""
Điểm khởi chạy chương trình mô phỏng Underworld v0 - PR #3.
"""

import os
from typing import List, Optional, Dict, Any
from underworld.world.world import World
from underworld.world.state import WorldState
from underworld.human.human import Human
from underworld.engine.event_loop import EventLoop
from underworld.interface.observation import Observation
from underworld.interface.action import Action
from underworld.interface.quan_tri_vien import QuanTriVien
from underworld.data.dataset import Dataset


class DemoQuanTriVien(QuanTriVien):
    """
    Quản trị viên minh họa: quan sát ở MỖI bước thời gian và đưa ra các quyết định
    can thiệp quản trị hoặc yêu cầu dừng thế giới.
    """

    def __init__(self, name: str = "Quản_Trị_Viên_Tối_Cao"):
        super().__init__(name=name)
        self.so_lan_goi = 0

    def tai_moi_buoc(self, trang_thai_the_gioi: WorldState) -> List[Dict[str, Any]]:
        self.so_lan_goi += 1
        t = trang_thai_the_gioi.time_step
        print(f"  [QUẢN TRỊ VIÊN] Bước t={t}: Gọi lần thứ {self.so_lan_goi} để kiểm tra trạng thái thế giới.")

        # Ví dụ can thiệp ở bước t = 3: Thay đổi thời tiết môi trường
        if t == 3:
            print("  [QUẢN TRỊ VIÊN] Can thiệp: Thay đổi thời tiết thành 'mưa_bão'.")
            return [{
                "loai_lenh": "THAY_DOI_MOI_TRUONG",
                "key": "weather",
                "val": "mưa_bão"
            }]

        # Ví dụ can thiệp ở bước t = 7: Yêu cầu dừng mô phỏng thế giới
        if t == 7:
            print("  [QUẢN TRỊ VIÊN] Quyết định: Yêu cầu DỪNG mô phỏng thế giới.")
            self.yeu_cau_dung()
            return [{
                "loai_lenh": "YEU_CAU_DUNG"
            }]

        return []


def external_agent_brain(observation: Observation) -> Optional[List[Action]]:
    """
    Agent bên ngoài minh họa ranh giới giao tiếp (Observation -> Action).

    Ở bước time_step == 5, Agent gửi một hành động can thiệp ép Human_001 nghỉ ngơi.
    """
    if observation.time_step == 5:
        print(f"  [EXTERNAL AGENT] Quan sát thấy time_step={observation.time_step}. Gửi lệnh REST cho Human_001!")
        return [
            Action(
                action_type="REST",
                target_id="Human_001",
                payload={"reason": "Tác động từ External Agent"}
            )
        ]
    return None


def run_simulation():
    """
    Chạy minh họa toàn bộ pipeline mô phỏng Underworld v0 với Quản trị viên:
    World -> WorldState -> N x Human -> Event Loop -> Observation / Action / QuanTriVien -> Trajectory -> Dataset
    """
    print("=" * 70)
    print("      KHỞI ĐỘNG UNDERWORLD v0 - PYTHON SIMULATION SKELETON (PR #3)")
    print("=" * 70)

    # 1. Khởi tạo World với hạt giống ngẫu nhiên để tái lập
    world = World(bounds=(50, 50), seed=42)

    # 2. Khởi tạo 3 Human
    human_1 = Human(human_id="Human_001", position=(0, 0), status="sẵn_sàng")
    human_2 = Human(human_id="Human_002", position=(1, 0), status="sẵn_sàng")
    human_3 = Human(human_id="Human_003", position=(10, 10), status="sẵn_sàng")

    world.add_human(human_1)
    world.add_human(human_2)
    world.add_human(human_3)

    print(f"\n[1] Đã khởi tạo World (Hạt giống seed=42) với {len(world.humans)} Human:")
    for hid, h in world.humans.items():
        st = h.get_state()
        print(f"    - {hid}: vị trí={st.position}, trạng thái={st.status}")

    # 3. Khởi tạo Quản trị viên và Event Loop
    quan_tri_vien = DemoQuanTriVien()
    event_loop = EventLoop(world)
    dataset = Dataset()

    print("\n------------------------------------------------------------")
    print("[2] TIẾN HÀNH MÔ PHỎNG: Quản trị viên can thiệp ở MỖI bước")
    print("------------------------------------------------------------")

    # Chạy mô phỏng vô hạn (so_buoc=None) - sẽ tự kết thúc khi Quản trị viên gửi yeu_cau_dung()
    trajectory = event_loop.chay(
        so_buoc=None,
        quan_tri_vien=quan_tri_vien,
        agent_callback=external_agent_brain,
        trajectory_id="traj_demo_pr3"
    )

    for step in trajectory.steps:
        print(f"\n---> Bước thời gian: {step.step}")
        for event in step.state_after["events"]:
            print(f"     Sự kiện: {event.get('chi_tiết')}")

    dataset.add_trajectory(trajectory)

    # 4. Xuất Dataset ra tệp JSONL
    output_dir = "data_output"
    os.makedirs(output_dir, exist_ok=True)
    dataset_path = os.path.join(output_dir, "dataset.jsonl")
    dataset.export_jsonl(dataset_path)

    print("\n============================================================")
    print("                   MÔ PHỎNG HOÀN THÀNH")
    print(f"  - Quản trị viên đã được gọi tổng cộng: {quan_tri_vien.so_lan_goi} lần.")
    print(f"  - Tổng số bước mô phỏng thực hiện: {len(trajectory.steps)} bước.")
    print(f"  - Đã xuất Dataset thành công tại: {dataset_path}")
    print("============================================================\n")


if __name__ == "__main__":
    run_simulation()
