"""
Điểm khởi chạy chương trình mô phỏng Underworld v0.
"""

import os
from typing import List, Optional
from underworld.world.world import World
from underworld.human.human import Human
from underworld.engine.event_loop import EventLoop
from underworld.interface.observation import Observation
from underworld.interface.action import Action
from underworld.data.dataset import Dataset


def external_agent_brain(observation: Observation) -> Optional[List[Action]]:
    """
    Agent bên ngoài minh họa ranh giới giao tiếp (Observation -> Action).

    Ở lượt time_step == 7, Agent gửi một hành động can thiệp ép Human_001 nghỉ ngơi.
    """
    if observation.time_step == 6:
        print(f"  [EXTERNAL AGENT] Quan sát thấy time_step={observation.time_step}. Gửi lệnh REST cho Human_001!")
        return [
            Action(
                action_type="REST",
                target_id="Human_001",
                payload={"reason": "Can thiệp ngoại cảnh từ Agent bên ngoài"}
            )
        ]
    return None


def run_simulation():
    """
    Chạy minh họa toàn bộ pipeline mô phỏng Underworld v0:
    World -> WorldState -> N x Human -> Event Loop -> Observation / Action -> Trajectory -> Dataset
    """
    print("=" * 60)
    print("           KHỞI ĐỘNG UNDERWORLD v0 - PYTHON SIMULATION")
    print("=" * 60)

    # 1. Khởi tạo World
    world = World(bounds=(50, 50))

    # 2. Tạo N x Human tại các vị trí khác nhau
    human_1 = Human(human_id="Human_001", position=(0, 0), status="sẵn_sàng")
    human_2 = Human(human_id="Human_002", position=(1, 0), status="sẵn_sàng")
    human_3 = Human(human_id="Human_003", position=(10, 10), status="sẵn_sàng")

    world.add_human(human_1)
    world.add_human(human_2)
    world.add_human(human_3)

    print(f"\n[1] Đã khởi tạo World với {len(world.humans)} Human:")
    for hid, h in world.humans.items():
        st = h.get_state()
        print(f"    - {hid}: vị trí={st.position}, trạng thái={st.status}")

    # 3. Khởi tạo Event Loop
    event_loop = EventLoop(world)
    dataset = Dataset()

    # PHẦN A: Thế giới tự chạy 5 bước không cần Agent bên ngoài
    print("\n------------------------------------------------------------")
    print("[2] GIAI ĐOẠN 1: Thế giới tự vận hành độc lập (Không có Agent)")
    print("------------------------------------------------------------")

    traj_autonomous = event_loop.run(steps=5, trajectory_id="traj_tu_van_hanh")

    for step in traj_autonomous.steps:
        print(f"\n---> Thời gian: {step.step}")
        for event in step.state_after["events"]:
            print(f"     Sự kiện: {event.get('chi_tiết')}")

    dataset.add_trajectory(traj_autonomous)

    # PHẦN B: Thế giới tiếp tục chạy 5 bước với Agent bên ngoài can thiệp qua Observation/Action
    print("\n------------------------------------------------------------")
    print("[3] GIAI ĐOẠN 2: Thế giới vận hành với External Agent (Tác động ngoại cảnh)")
    print("------------------------------------------------------------")

    traj_interactive = event_loop.run(
        steps=5,
        trajectory_id="traj_co_agent",
        agent_callback=external_agent_brain
    )

    for step in traj_interactive.steps:
        print(f"\n---> Thời gian: {step.step}")
        for event in step.state_after["events"]:
            print(f"     Sự kiện: {event.get('chi_tiết')}")

    dataset.add_trajectory(traj_interactive)

    # 4. Xuất Dataset ra tập tin JSONL
    output_dir = "data_output"
    os.makedirs(output_dir, exist_ok=True)
    dataset_path = os.path.join(output_dir, "dataset.jsonl")
    dataset.export_jsonl(dataset_path)

    print("\n============================================================")
    print("                   MÔ PHỎNG HOÀN THÀNH")
    print(f"  - Đã ghi lại {len(dataset.trajectories)} Trajectories.")
    print(f"  - Đã xuất Dataset thành công tại: {dataset_path}")
    print("============================================================\n")


if __name__ == "__main__":
    run_simulation()
