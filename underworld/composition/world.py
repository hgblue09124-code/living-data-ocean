"""
Mô-đun Composition hợp thành World từ các Atomic Modules.
"""

import copy
from typing import Dict, List, Any, Optional
from underworld.kernel.time import SimulationTime
from underworld.kernel.randomness import Randomness
from underworld.modules.environment import EnvironmentState
from underworld.modules.event import EventLog
from underworld.composition.human import Human
from underworld.world.state import WorldState


class World:
    """
    World là Composition root của thế giới mô phỏng.
    World tổng hợp và điều phối các Atomic Modules thông qua cơ chế Delegation:
    - SimulationTime: Quản lý thời gian
    - Randomness: Quản lý hạt giống ngẫu nhiên
    - EnvironmentState: Quản lý thuộc tính môi trường
    - EventLog: Quản lý nhật ký và vòng đời sự kiện
    - Dict[str, Human]: Quản lý danh sách các thực thể con người
    """

    def __init__(self, bounds: tuple = (100, 100), seed: Optional[int] = None):
        """Khởi tạo thế giới Underworld bằng Composition."""
        self.time = SimulationTime()
        self.environment_state = EnvironmentState(bounds=bounds)
        self.randomness = Randomness(seed=seed)
        self.event_log = EventLog()
        self.humans: Dict[str, Human] = {}

    @property
    def time_step(self) -> int:
        """Hỗ trợ truy cập time_step tương thích ngược."""
        return self.time.time_step

    @property
    def environment(self) -> Dict[str, Any]:
        """Hỗ trợ truy cập dict môi trường tương thích ngược."""
        return self.environment_state.to_dict()

    @property
    def events(self) -> List[Dict[str, Any]]:
        """Hỗ trợ truy cập danh sách events tương thích ngược."""
        return self.event_log.events

    def dat_hat_giong(self, seed: int) -> None:
        """Đặt hạt giống ngẫu nhiên."""
        self.randomness.set_seed(seed)

    def add_human(self, human: Human) -> None:
        """Thêm một Human vào thế giới."""
        self.humans[human.identity.id] = human

    def get_human(self, human_id: str) -> Optional[Human]:
        """Lấy thực thể Human theo ID."""
        return self.humans.get(human_id)

    def tao_su_kien(self, chi_tiet: str, loai_su_kien: str = "SU_KIEN_QUAN_TRI") -> None:
        """Ủy quyền tạo sự kiện cho EventLog."""
        self.event_log.add_event(chi_tiet, event_type=loai_su_kien)

    def apply_command(self, command: Any) -> None:
        """
        Ủy quyền xử lý lệnh từ AdministratorCommand đến từng Atomic Module thích hợp.
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
                self.environment_state.set_attribute(key, val)
        elif cmd_type in ("CREATE_EVENT", "TAO_SU_KIEN"):
            detail = payload.get("detail", payload.get("chi_tiet", "Sự kiện từ Administrator"))
            self.event_log.add_event(detail, event_type="SU_KIEN_QUAN_TRI")
        elif cmd_type in ("AFFECT_HUMAN", "TAC_DONG_CON_NGUOI"):
            if target_id:
                human = self.get_human(target_id)
                if human:
                    action_type = payload.get("action_type", "REST")
                    action_payload = payload.get("payload", {})
                    human.apply_external_action(action_type, action_payload)

    def get_state(self) -> WorldState:
        """Trả về snapshot WorldState độc lập (deep copy) tại thời điểm t hiện tại."""
        human_states = {hid: h.get_state() for hid, h in self.humans.items()}
        return WorldState(
            time_step=self.time.time_step,
            human_states=human_states,
            environment=self.environment_state.to_dict(),
            events=self.event_log.to_list()
        )

    def tick(self, external_actions: Optional[List[Dict[str, Any]]] = None) -> WorldState:
        """
        Thực hiện chuyển trạng thái thế giới: WorldState(t) -> WorldState(t+1).
        - Tiến thời gian 1 bước
        - Chuẩn bị và bảo tồn sự kiện bước hiện tại qua EventLog
        - Duyệt qua từng Human và ủy quyền thực hiện hành động
        - Phát hiện tương tác ngẫu nhiên giữa các Human ở gần vị trí nhau
        """
        # Tăng time_step thêm 1 bước
        current_step = self.time.increment()

        # Chuẩn bị sự kiện cho bước mới qua EventLog
        self.event_log.prepare_step_events(current_step)

        # Ánh xạ external actions
        action_map: Dict[str, Dict[str, Any]] = {}
        if external_actions:
            for act in external_actions:
                target_id = act.get("target_id")
                if target_id:
                    action_map[target_id] = act

        # Cho từng Human tự do hành động hoặc nhận lệnh
        for human_id, human in self.humans.items():
            if human_id in action_map:
                ext_act = action_map[human_id]
                action_type = ext_act.get("action_type", "UNKNOWN")
                payload = ext_act.get("payload", {})
                action_taken = human.apply_external_action(action_type, payload)
                self.event_log.record_processed_event({
                    "time_step": current_step,
                    "type": "TAC_DONG_NGOAI",
                    "human_id": human_id,
                    "chi_tiết": f"Tác động ngoại cảnh '{action_type}': {action_taken}"
                })
            else:
                action_taken = human.step({
                    "environment": self.environment_state.to_dict(),
                    "random": self.randomness
                })
                self.event_log.record_processed_event({
                    "time_step": current_step,
                    "type": "HANH_DONG_TU_CHU",
                    "human_id": human_id,
                    "chi_tiết": f"Human {human_id} tự thực hiện: {action_taken}"
                })

        # Xử lý tương tác ngẫu nhiên giữa các Human qua SpatialSpace distance
        human_list = list(self.humans.values())
        for i in range(len(human_list)):
            for j in range(i + 1, len(human_list)):
                h1, h2 = human_list[i], human_list[j]
                dist = h1.spatial.manhattan_distance(h2.spatial.position)
                if dist <= 1:
                    self.event_log.record_processed_event({
                        "time_step": current_step,
                        "type": "TUONG_TAC_HUMAN",
                        "human_1": h1.identity.id,
                        "human_2": h2.identity.id,
                        "chi_tiết": f"Human {h1.identity.id} và Human {h2.identity.id} gặp gỡ tại {h1.spatial.position}"
                    })
                    h1.needs.needs["xã_hội"] = min(100.0, h1.needs.needs["xã_hội"] + 10.0)
                    h2.needs.needs["xã_hội"] = min(100.0, h2.needs.needs["xã_hội"] + 10.0)
                    h1.needs.status = "gặp_gỡ"
                    h2.needs.status = "gặp_gỡ"

        return self.get_state()
