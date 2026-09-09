"""
Mô-đun Atomic tiếp nhận và phân phối AdministratorCommand (CommandDispatcher).
"""

from typing import Dict, Any, Optional
from underworld.modules.environment import EnvironmentState
from underworld.modules.event import EventLog


class CommandDispatcher:
    """
    Sở hữu capability phân phối các lệnh AdministratorCommand từ bên ngoài tới các mô-đun chức năng thích hợp
    (EnvironmentState, EventLog, Human).
    """

    def dispatch(
        self,
        command: Any,
        environment: EnvironmentState,
        event_log: EventLog,
        humans_map: Dict[str, Any]
    ) -> None:
        """
        Phân phối và áp dụng lệnh lên các mô-đun tương ứng.
        """
        if hasattr(command, "command_type"):
            cmd_type = command.command_type
            payload = getattr(command, "payload", {})
            target_id = getattr(command, "target_id", None)
        elif isinstance(command, dict):
            cmd_type = command.get("command_type", command.get("loai_lenh"))
            payload = command.get("payload", command)
            target_id = command.get("target_id")
        else:
            return

        if cmd_type in ("CHANGE_ENVIRONMENT", "THAY_DOI_MOI_TRUONG"):
            key = payload.get("key")
            val = payload.get("val")
            if key is not None:
                environment.set_attribute(key, val)
        elif cmd_type in ("CREATE_EVENT", "TAO_SU_KIEN"):
            detail = payload.get("detail", payload.get("chi_tiet", "Sự kiện từ Administrator"))
            event_log.add_event(detail, event_type="SU_KIEN_QUAN_TRI")
        elif cmd_type == "CREATE_HUMAN":
            # Khởi tạo linh hoạt để tránh phụ thuộc vòng giữa modules và composition
            from underworld.composition.human import Human
            new_idx = len(humans_map) + 1
            new_id = f"Human_{new_idx:03d}"
            pos = payload.get("position", (new_idx * 3, new_idx * 3))
            new_h = Human(human_id=new_id, position=pos, status="mới_xuất_hiện")
            humans_map[new_id] = new_h
            event_log.add_event(f"Tạo thành công con người mới '{new_id}' tại vị trí {pos}", event_type="SU_KIEN_QUAN_TRI")
        elif cmd_type == "TRIGGER_DISASTER":
            disaster_name = payload.get("disaster", "Bão Thiên Tai")
            environment.set_attribute("weather", disaster_name)
            event_log.add_event(f"THIÊN TAI BỘC PHÁT: {disaster_name} giáng xuống thế giới!", event_type="SU_KIEN_THIEN_TAI")
        elif cmd_type in ("AFFECT_HUMAN", "TAC_DONG_CON_NGUOI"):
            if target_id and target_id in humans_map:
                human = humans_map[target_id]
                action_type = payload.get("action_type", "REST")
                action_payload = payload.get("payload", {})
                human.apply_external_action(action_type, action_payload)
