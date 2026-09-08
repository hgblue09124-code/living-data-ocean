"""
Định nghĩa đối tượng World sở hữu và quản lý vòng đời thế giới Underworld.
"""

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

    def __init__(self, bounds: tuple = (100, 100)):
        """Khởi tạo thế giới Underworld."""
        self.time_step: int = 0
        self.humans: Dict[str, Human] = {}
        self.environment: Dict[str, Any] = {
            "bounds": bounds,
            "weather": "bình_thường",
            "resources": {"thức_ăn": 50, "nước": 50}
        }
        self.events: List[Dict[str, Any]] = []

    def add_human(self, human: Human) -> None:
        """Thêm một Human vào thế giới."""
        self.humans[human.state.id] = human

    def get_human(self, human_id: str) -> Optional[Human]:
        """Lấy thực thể Human theo ID."""
        return self.humans.get(human_id)

    def get_state(self) -> WorldState:
        """Trả về snapshot WorldState tại thời điểm t hiện tại."""
        human_states = {hid: h.get_state() for hid, h in self.humans.items()}
        return WorldState(
            time_step=self.time_step,
            human_states=human_states,
            environment=dict(self.environment),
            events=list(self.events)
        )

    def tick(self, external_actions: Optional[List[Dict[str, Any]]] = None) -> WorldState:
        """
        Thực hiện một bước tiến thời gian (tick): WorldState(t) -> WorldState(t+1).

        1. Cập nhật thời gian t = t + 1.
        2. Xử lý các tác động/hành động bên ngoài (nếu có).
        3. Cho tất cả Human tự do hành động nếu không có can thiệp ngoại cảnh.
        4. Phát hiện tương tác ngẫu nhiên giữa các Human (ví dụ: gặp gỡ khi ở gần).
        5. Cập nhật WorldState mới.
        """
        self.time_step += 1
        self.events = []

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
                    "chi_tiết": f"Tác động ngoại cảnh '{action_type}': {action_taken}"
                })
            else:
                # Human tự vận hành theo logic nội tại
                action_taken = human.step({"environment": self.environment})
                self.events.append({
                    "time_step": self.time_step,
                    "type": "HANH_DONG_TU_CHU",
                    "human_id": human_id,
                    "chi_tiết": f"Human {human_id} tự thực hiện: {action_taken}"
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
                        "chi_tiết": f"Human {h1.state.id} và Human {h2.state.id} gặp gỡ tại {h1.state.position}"
                    }
                    self.events.append(interaction_event)
                    # Cập nhật chỉ số xã hội cho cả hai Human
                    h1.state.needs["xã_hội"] = min(100.0, h1.state.needs["xã_hội"] + 10.0)
                    h2.state.needs["xã_hội"] = min(100.0, h2.state.needs["xã_hội"] + 10.0)
                    h1.state.status = "gặp_gỡ"
                    h2.state.status = "gặp_gỡ"

        return self.get_state()
