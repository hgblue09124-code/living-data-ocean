"""
Điểm khởi chạy chương trình mô phỏng Underworld v0 - PR #3 (Refactored Boundary).
"""

import os
from typing import List, Optional
from underworld.world.world import World
from underworld.human.human import Human
from underworld.engine.event_loop import EventLoop
from underworld.interface.observation import Observation
from underworld.interface.action import Action
from underworld.interface.administrator import Administrator
from underworld.data.dataset import Dataset


def external_agent_brain(observation: Observation) -> Optional[List[Action]]:
    """
    External Agent minh họa ranh giới giao tiếp (Observation -> Action).

    Ở bước time_step == 5, Agent gửi một Action ép Human_001 nghỉ ngơi.
    """
    if observation.time_step == 5:
        print(f"  [EXTERNAL AGENT] Quan sát thấy time_step={observation.time_step}. Gửi lệnh Action 'REST' cho Human_001!")
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
    Chạy minh họa toàn bộ pipeline mô phỏng Underworld v0:
    Administrator UI/Interface -> AdministratorCommand -> Runtime -> World -> WorldState
    """
    print("=" * 75)
    print("   KHỞI ĐỘNG UNDERWORLD v0 - PYTHON SIMULATION SKELETON (BOUNDARY REFACTORED)")
    print("=" * 75)

    # 1. Khởi tạo World với hạt giống ngẫu nhiên để tái lập
    world = World(bounds=(50, 50), seed=42)

    # 2. Khởi tạo 3 Human
    human_1 = Human(human_id="Human_001", position=(0, 0), status="sẵn_sàng")
    human_2 = Human(human_id="Human_002", position=(1, 0), status="sẵn_sàng")
    human_3 = Human(human_id="Human_003", position=(10, 10), status="sẵn_sàng")

    world.add_human(human_1)
    world.add_human(human_2)
    world.add_human(human_3)

    print(f"\n[1] Đã khởi tạo World (Seed=42) với {len(world.humans)} Human:")
    for hid, h in world.humans.items():
        st = h.get_state()
        print(f"    - {hid}: vị trí={st.position}, trạng thái={st.status}")

    # 3. Khởi tạo Administrator (Đứng ngoài thế giới) và Event Loop (Runtime)
    admin = Administrator(name="System_Administrator")
    event_loop = EventLoop(world)
    dataset = Dataset()

    # Quản trị viên gửi một số lệnh can thiệp từ bên ngoài qua Interface
    print("\n[2] Administrator tạo các lệnh can thiệp từ bên ngoài (Control Interface):")
    admin.change_environment("weather", "mưa_bão")
    print("    - Lệnh 1: change_environment('weather', 'mưa_bão')")
    admin.create_event("Thiên thạch rơi gần vĩ độ (0,0)")
    print("    - Lệnh 2: create_event('Thiên thạch rơi gần vĩ độ (0,0)')")

    print("\n------------------------------------------------------------")
    print("[3] TIẾN HÀNH MÔ PHỎNG: Runtime thực thi bước và nhận tác động")
    print("------------------------------------------------------------")

    # Chạy mô phỏng 7 bước với Administrator và External Agent
    trajectory = event_loop.run(
        steps=7,
        administrator=admin,
        agent_callback=external_agent_brain,
        trajectory_id="traj_demo_refactored"
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
    print(f"  - Tổng số bước mô phỏng thực hiện: {len(trajectory.steps)} bước.")
    print(f"  - Đã xuất Dataset thành công tại: {dataset_path}")
    print("============================================================\n")


if __name__ == "__main__":
    run_simulation()
