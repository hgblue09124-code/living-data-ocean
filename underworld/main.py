"""Điểm khởi chạy chương trình mô phỏng Underworld v0 với World Graphics Web UI.

Kiến trúc luồng xử lý:
  Modules -> World -> World Program -> World Graphics -> UI Program -> Web UI Program
"""

import sys
import os
import argparse
from typing import List, Any, Dict, Optional

# Nạp các Modules mô phỏng
from underworld.modules.spatial import SpatialSpace
from underworld.modules.environment import EnvironmentState
from underworld.modules.entity import EntityNeeds
from underworld.modules.event import EventLog
from underworld.modules.behavior import EntityBehavior
from underworld.modules.interaction import InteractionRule
from underworld.modules.command_dispatcher import CommandDispatcher
from underworld.modules.command_intake import CommandIntakeModule
from underworld.modules.observation_builder import ObservationBuilderModule
from underworld.modules.action_resolver import ActionResolverModule
from underworld.modules.stop_policy import StopPolicyModule
from underworld.modules.trajectory_recorder import TrajectoryRecorderModule
from underworld.modules.meso.simulation_engine import SimulationEngineMeso

# Nạp các UI Modules, World Graphics & Web Server
from underworld.modules.ui import (
    WorldStateViewModule,
    EntityViewModule,
    EventViewModule,
    TimelineViewModule,
    SimulationControlViewModule,
)
from underworld.composition.world_program import WorldProgram
from underworld.graphics.world_graphics import WorldGraphics
from underworld.graphics.web_server import start_web_server
from underworld.interface.administrator import Administrator, AdministratorCommand


def build_ecosystem_modules() -> List[Any]:
    """Khởi tạo toàn bộ Hệ sinh thái Modules (Atomic, Meso & UI Modules)."""
    return [
        # Domain Modules / Classes
        SpatialSpace(),
        EnvironmentState(),
        EntityNeeds(),
        EventLog(),
        EntityBehavior(),
        InteractionRule(),
        CommandDispatcher(),
        CommandIntakeModule(),
        ObservationBuilderModule(),
        ActionResolverModule(),
        StopPolicyModule(),
        TrajectoryRecorderModule(),
        SimulationEngineMeso(),
        # UI Modules
        WorldStateViewModule(),
        EntityViewModule(),
        EventViewModule(),
        TimelineViewModule(),
        SimulationControlViewModule(),
    ]


def run_simulation(headless: bool = False, web: bool = False, port: int = 8000, ticks: int = 5):
    """Khởi chạy mô phỏng Underworld v0 qua World Program và World Graphics.

    Args:
        headless: Nếu True, chạy ở chế độ console không hiển thị Web Server.
        web: Nếu True, khởi chạy Web UI Server cho trình duyệt/di động.
        port: Cổng lắng nghe của Web UI Server.
        ticks: Số bước tick cần chạy trong chế độ headless.
    """
    print("=" * 80)
    print("   UNDERWORLD v0 — WEB UI PROGRAM VIA WORLD GRAPHICS")
    print("=" * 80)

    # 1. Thu thập Modules Ecosystem
    available_modules = build_ecosystem_modules()
    print(f"\n[1] Hệ sinh thái Modules: Tổng số {len(available_modules)} Modules đã nạp.")

    # 2. Tổng hợp World Program (Executable Program) từ Modules
    world_program = WorldProgram.assemble(
        available_modules=available_modules,
        world_seed=42,
        num_humans=3
    )
    print("[2] Đã tổng hợp World Program (Substrate: World | Runtime: EventLoop)")

    # 3. Khởi tạo World Graphics
    world_graphics = WorldGraphics(available_modules=available_modules)

    # Lựa chọn trật tự layout giao diện động thông qua World Graphics
    desired_layout = [
        "ui_world_state_view",
        "ui_simulation_control_view",
        "ui_entity_view",
        "ui_event_view",
        "ui_timeline_view"
    ]

    # 4. World Graphics thực hiện: Filter -> Order -> Compose -> UIProgram
    ui_program = world_graphics.compose_ui_program(
        layout_order=desired_layout,
        title="Underworld v0 — World Graphics Web UI"
    )
    print(f"[3] World Graphics đã tổng hợp UI Program với {len(ui_program.ui_modules)} UI Modules.")

    # Kiểm tra cờ Headless hoặc mặc định nếu không yêu cầu --web
    is_headless_mode = headless or not web or os.environ.get("HEADLESS") == "1"

    if is_headless_mode:
        print("\n------------------------------------------------------------")
        print("[4] BẮT ĐẦU MÔ PHỎNG Ở CHẾ ĐỘ HEADLESS / CONSOLE RUNTIME")
        print("------------------------------------------------------------")
        for i in range(ticks):
            state = world_program.run_step()
            tick = state.get("time_step", 0)
            env = state.get("environment", {})
            humans_cnt = len(state.get("human_states", state.get("humans", {})))
            print(f"  --> [Tick {tick}] Thời tiết: {env.get('weather')} | Số con người: {humans_cnt}")
        print("\n============================================================")
        print("                   MÔ PHỎNG HEADLESS HOÀN THÀNH")
        print("============================================================\n")
        return

    # Khởi chạy Web UI Server cho trình duyệt di động / desktop
    print("\n------------------------------------------------------------")
    print(f"[4] BẮT ĐẦU WEB UI SERVER TẠI HOẠT ĐỘNG TẠI: http://0.0.0.0:{port}")
    print(f"    Có thể mở từ trình duyệt iPhone/Safari/Chrome trên cùng mạng local!")
    print("------------------------------------------------------------")

    admin = Administrator(name="Web_Operator")
    server = start_web_server(
        world_program=world_program,
        ui_program=ui_program,
        admin=admin,
        host="0.0.0.0",
        port=port
    )

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã dừng Web UI Server.")
    finally:
        server.server_close()


def main():
    parser = argparse.ArgumentParser(description="Underworld v0 Simulation Engine & Web UI Program")
    parser.add_argument("--web", action="store_true", help="Khởi chạy Web UI Server truy cập từ trình duyệt/di động")
    parser.add_argument("--headless", action="store_true", help="Chạy ở chế độ không mở Web Server")
    parser.add_argument("--port", type=int, default=8000, help="Cổng chạy Web UI Server")
    parser.add_argument("--ticks", type=int, default=5, help="Số ticks chạy trong chế độ headless")
    args = parser.parse_args()

    run_simulation(headless=args.headless, web=args.web, port=args.port, ticks=args.ticks)


if __name__ == "__main__":
    main()
