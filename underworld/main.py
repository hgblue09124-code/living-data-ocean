"""
Điểm khởi chạy chương trình mô phỏng Underworld v0 - Control Loop Session Demo.
"""

import os
from typing import List, Optional, Dict, Any
from underworld.composition import World, Human
from underworld.runtime import EventLoop
from underworld.interface import Observation, Action, Administrator, AdministratorCommand
from underworld.data import Dataset


def external_agent_brain(observation: Observation) -> Optional[List[Action]]:
    """
    External Agent minh họa ranh giới giao tiếp (Observation -> Action).

    Ở bước time_step == 4, Agent gửi một Action ép Human_001 nghỉ ngơi.
    """
    if observation.time_step == 4:
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
    Chạy minh họa toàn bộ pipeline mô phỏng Underworld v0 với Control Loop Session:
    World -> Runtime Start -> World Advances -> Administrator Control Session (Run N ticks, Command, Observe, Stop)
    """
    print("=" * 80)
    print("   KHỞI ĐỘNG UNDERWORLD v0 - CONTROL LOOP SESSION DEMO (PR #3)")
    print("=" * 80)

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

    # Kịch bản các giai đoạn điều khiển của Administrator trong phiên làm việc
    session_phases = [
        {"giai_đoạn": "1. Khởi động", "action": "RUN_N_TICKS", "ticks": 2},
        {
            "giai_đoạn": "2. Tác động quản trị",
            "action": "COMMAND",
            "commands": [
                AdministratorCommand("CHANGE_ENVIRONMENT", {"key": "weather", "val": "mưa_bão"}),
                AdministratorCommand("CREATE_EVENT", {"detail": "Thiên thạch rơi gần vĩ độ (0,0)"})
            ]
        },
        {"giai_đoạn": "3. Tiếp tục mô phỏng", "action": "RUN_N_TICKS", "ticks": 3},
        {"giai_đoạn": "4. Dừng mô phỏng", "action": "STOP"}
    ]
    phase_index = 0

    def administrator_session_controller(world_state) -> Dict[str, Any]:
        nonlocal phase_index
        if phase_index < len(session_phases):
            p = session_phases[phase_index]
            phase_index += 1
            print(f"\n  [ADMINISTRATOR CONTROL SESSION] {p['giai_đoạn']}: Lựa chọn hành động '{p['action']}'")
            return p
        return {"action": "STOP"}

    print("\n------------------------------------------------------------")
    print("[2] BẮT ĐẦU PHIÊN ĐIỀU KHIỂN CONTROL LOOP SỐNG CỦA ADMINISTRATOR")
    print("------------------------------------------------------------")

    # Chạy phiên mô phỏng với Control Loop tương tác đa giai đoạn
    trajectory = event_loop.run_session(
        session_controller=administrator_session_controller,
        administrator=admin,
        agent_callback=external_agent_brain,
        trajectory_id="traj_control_loop_demo"
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
    print(f"  - Tổng số bước mô phỏng thực hiện trong phiên: {len(trajectory.steps)} bước.")
    print(f"  - Đã xuất Dataset thành công tại: {dataset_path}")
    print("============================================================\n")


if __name__ == "__main__":
    run_simulation()
