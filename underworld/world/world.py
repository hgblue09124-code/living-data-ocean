"""
Định nghĩa đối tượng World sở hữu và quản lý vòng đời thế giới Underworld.
"""

import copy
import random
from typing import Dict, List, Any, Optional
from underworld.human.human import Human
from underworld.human.state import HumanState
from underworld.world.state import WorldState


class World:
    """
    Thế giới mô phỏng Underworld.

    World sở hữu trạng thái thế giới (WorldState), danh sách các Human,
    môi trường và chịu trách nhiệm thực hiện chuyển trạng thái:
    WorldState(t) -> events -> WorldState(t+1) thông qua hàm `tick()`.
    """

    def __init__(self, bounds: tuple = (100, 100), seed: Optional[int] = None):
        """Khởi tạo thế giới Underworld với tùy chọn hạt giống ngẫu nhiên."""
        self.time_step: int = 0
        self.humans: Dict[str, Human] = {}
        self.environment: Dict[str, Any] = {
            "bounds": bounds,
            "weather": "bình_thường",
            "resources": {"thức_ăn": 50, "nước": 50}
        }
        self.events: List[Dict[str, Any]] = []
        self.rng = random.Random(seed) if seed is not None else random.Random()

    def dat_hat_giong(self, seed: int) -> None:
        """Thiết lập hạt giống ngẫu nhiên phục vụ tính tái lập."""
        self.rng = random.Random(seed)
        random.seed(seed)

    def add_human(self, human: Human) -> None:
        """Thêm một Human vào thế giới."""
        self.humans[human.state.id] = human

    def get_human(self, human_id: str) -> Optional[Human]:
        """Lấy thực thể Human theo ID."""
        return self.humans.get(human_id)

    def tao_su_kien(self, chi_tiet: str, loai_su_kien: str = "SU_KIEN_QUAN_TRI") -> None:
        """Thêm một sự kiện ngoài/quản trị vào danh sách chờ xử lý cho bước tiếp theo."""
        self.events.append({
            "type": loai_su_kien,
            "chi_tiết": chi_tiet,
            "processed": False
        })

    def apply_command(self, command: Any) -> None:
        """
        Áp dụng một AdministratorCommand trung gian từ bên ngoài vào thế giới.
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
                self.environment[key] = val
        elif cmd_type in ("CREATE_EVENT", "TAO_SU_KIEN"):
            detail = payload.get("detail", payload.get("chi_tiet", "Sự kiện từ Administrator"))
            self.tao_su_kien(detail, loai_su_kien="SU_KIEN_QUAN_TRI")
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
            time_step=self.time_step,
            human_states=human_states,
            environment=copy.deepcopy(self.environment),
            events=copy.deepcopy(self.events)
        )

    def tick(self, external_actions: Optional[List[Dict[str, Any]]] = None) -> WorldState:
        """
        Thực hiện một bước tiến thời gian (tick): WorldState(t) -> WorldState(t+1).

        1. Bảo tồn các sự kiện do Administrator/Ngoại cảnh tạo ra trước tick cho lượt này.
        2. Cập nhật thời gian t = t + 1.
        3. Xử lý các tác động/hành động bên ngoài (nếu có).
        4. Cho tất cả Human tự do hành động nếu không có can thiệp ngoại cảnh.
        5. Phát hiện tương tác ngẫu nhiên giữa các Human (ví dụ: gặp gỡ khi ở gần).
        6. Cập nhật WorldState mới.
        """
        # Thu thập các sự kiện chưa được xử lý (ví dụ do Administrator tạo ra trước tick)
        su_kien_truoc_tick = [e for e in self.events if not e.get("processed", False)]

        self.time_step += 1
        self.events = []

        # Đưa các sự kiện trước tick vào danh sách sự kiện bước hiện tại
        for sk in su_kien_truoc_tick:
            sk["time_step"] = self.time_step
            sk["processed"] = True
            self.events.append(sk)

        # Tạo ánh xạ các action bên ngoài theo target human_id
        action_map: Dict[str, Dict[str, Any]] = {}
        if external_actions:
            for act in external_actions:
                target_id = act.get("target_id")
                if target_id:
                    action_map[target_id] = act

        # Duyệt qua từng Human để thực hiện hành động
        for human_id, human in self.humans.items():
            if human_id in action_map:
                # Tác động từ bên ngoài can thiệp trực tiếp
                ext_act = action_map[human_id]
                action_type = ext_act.get("action_type", "UNKNOWN")
                payload = ext_act.get("payload", {})
                action_taken = human.apply_external_action(action_type, payload)
                self.events.append({
                    "time_step": self.time_step,
                    "type": "TAC_DONG_NGOAI",
                    "human_id": human_id,
                    "chi_tiết": f"Tác động ngoại cảnh '{action_type}': {action_taken}",
                    "processed": True
                })
            else:
                # Human tự vận hành theo logic nội tại
                action_taken = human.step({
                    "environment": self.environment,
                    "random": self.rng
                })
                self.events.append({
                    "time_step": self.time_step,
                    "type": "HANH_DONG_TU_CHU",
                    "human_id": human_id,
                    "chi_tiết": f"Human {human_id} tự thực hiện: {action_taken}",
                    "processed": True
                })

        # Phát hiện sự kiện tương tác giữa các Human ở gần vị trí nhau
        human_list = list(self.humans.values())
        for i in range(len(human_list)):
            for j in range(i + 1, len(human_list)):
                h1, h2 = human_list[i], human_list[j]
                # Tương tác nếu ở cùng vị trí hoặc khoảng cách Manhattan <= 1
                dist = abs(h1.state.position[0] - h2.state.position[0]) + abs(h1.state.position[1] - h2.state.position[1])
                if dist <= 1:
                    interaction_event = {
                        "time_step": self.time_step,
                        "type": "TUONG_TAC_HUMAN",
                        "human_1": h1.state.id,
                        "human_2": h2.state.id,
                        "chi_tiết": f"Human {h1.state.id} và Human {h2.state.id} gặp gỡ tại {h1.state.position}",
                        "processed": True
                    }
                    self.events.append(interaction_event)
                    # Cập nhật chỉ số xã hội cho cả hai Human
                    h1.state.needs["xã_hội"] = min(100.0, h1.state.needs["xã_hội"] + 10.0)
                    h2.state.needs["xã_hội"] = min(100.0, h2.state.needs["xã_hội"] + 10.0)
                    h1.state.status = "gặp_gỡ"
                    h2.state.status = "gặp_gỡ"

        return self.get_state()
