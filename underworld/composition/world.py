"""
Mô-đun Composition hợp thành World từ các Atomic Modules.
"""

import copy
from typing import Dict, List, Any, Optional
from underworld.kernel.time import SimulationTime
from underworld.kernel.randomness import Randomness
from underworld.modules.environment import EnvironmentState
from underworld.modules.event import EventLog
from underworld.modules.interaction import InteractionRule
from underworld.modules.command_dispatcher import CommandDispatcher
from underworld.composition.human import Human
from underworld.composition.state import WorldState


class World:
    """
    World là Composition root của thế giới mô phỏng.
    World đóng vai trò điều phối chính và ủy quyền (delegation) hoàn toàn cho các Atomic Modules:
    - SimulationTime: Quản lý thời gian
    - Randomness: Quản lý hạt giống ngẫu nhiên
    - EnvironmentState: Quản lý thuộc tính môi trường
    - EventLog: Quản lý nhật ký và vòng đời sự kiện
    - InteractionRule: Quản lý tương tác không gian giữa các thực thể
    - CommandDispatcher: Tiếp nhận và phân phối các lệnh AdministratorCommand
    - Dict[str, Human]: Quản lý danh sách các thực thể con người
    """

    def __init__(self, bounds: tuple = (100, 100), seed: Optional[int] = None):
        """Khởi tạo thế giới Underworld bằng Composition."""
        self.time = SimulationTime()
        self.environment_state = EnvironmentState(bounds=bounds)
        self.randomness = Randomness(seed=seed)
        self.event_log = EventLog()
        self.interaction_rule = InteractionRule()
        self.command_dispatcher = CommandDispatcher()
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
        Ủy quyền xử lý lệnh từ AdministratorCommand sang CommandDispatcher.
        """
        self.command_dispatcher.dispatch(
            command=command,
            environment=self.environment_state,
            event_log=self.event_log,
            humans_map=self.humans
        )

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
        - Tăng thời gian 1 bước qua SimulationTime
        - Chuẩn bị danh sách sự kiện qua EventLog
        - Cho từng Human tự vận hành hoặc áp dụng tác động bên ngoài
        - Ủy quyền xử lý tương tác giữa các Human qua InteractionRule
        """
        current_step = self.time.increment()
        self.event_log.prepare_step_events(current_step)

        # Ánh xạ external actions
        action_map: Dict[str, Dict[str, Any]] = {}
        if external_actions:
            for act in external_actions:
                target_id = act.get("target_id")
                if target_id:
                    action_map[target_id] = act

        # Duyệt từng Human để thực hiện bước mô phỏng
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

        # Ủy quyền xử lý tương tác qua InteractionRule
        human_list = list(self.humans.values())
        self.interaction_rule.process_interactions(
            humans_list=human_list,
            time_step=current_step,
            event_log=self.event_log
        )

        return self.get_state()
