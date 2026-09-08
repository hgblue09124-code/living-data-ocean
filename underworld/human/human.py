"""
Định nghĩa thực thể Human tồn tại và tự vận hành trong Underworld.
"""

import copy
import random
from typing import Dict, Any, Optional, Tuple
from underworld.human.state import HumanState


class Human:
    """
    Thực thể Human đại diện cho con người trong Underworld.

    Human sở hữu trạng thái nội tại (HumanState) và có khả năng
    tự động ra quyết định hành động dựa trên quy luật sinh học/nhu cầu
    mà không cần đến mô hình AI nặng hay agent bên ngoài.
    """

    def __init__(
        self,
        human_id: str,
        position: Tuple[int, int] = (0, 0),
        status: str = "thong_dong",
        needs: Optional[Dict[str, float]] = None,
        goals: Optional[list] = None
    ):
        """Khởi tạo một thực thể Human."""
        initial_needs = needs if needs is not None else {
            "năng_lượng": 100.0,
            "đói": 0.0,
            "xã_hội": 50.0
        }
        initial_goals = goals if goals is not None else ["khám_phá"]

        self.state = HumanState(
            id=human_id,
            position=position,
            status=status,
            needs=initial_needs,
            goals=initial_goals,
            memory=[],
            action_history=[]
        )

    def get_state(self) -> HumanState:
        """Trả về snapshot trạng thái độc lập (deep copy) hiện tại của Human."""
        return copy.deepcopy(self.state)

    def step(self, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Thực hiện một bước tự vận hành (tick nội tại) của Human.

        Cập nhật nhu cầu cơ bản, tự quyết định hành động tự nhiên dựa trên trạng thái
        và môi trường xung quanh. Trả về tên hành động đã thực hiện.
        """
        # Sử dụng bộ sinh số ngẫu nhiên từ context nếu có (phục vụ tính tái lập)
        rng = (context and context.get("random")) or random

        # Cập nhật chỉ số sinh học cơ bản qua thời gian
        self.state.needs["năng_lượng"] = max(0.0, self.state.needs["năng_lượng"] - 2.0)
        self.state.needs["đói"] = min(100.0, self.state.needs["đói"] + 3.0)
        self.state.needs["xã_hội"] = max(0.0, self.state.needs["xã_hội"] - 1.0)

        # Ra quyết định hành động tự chủ dựa trên nhu cầu
        action_taken = ""

        if self.state.needs["năng_lượng"] < 20.0:
            # Ưu tiên nghỉ ngơi phục hồi năng lượng
            self.state.status = "nghỉ_ngơi"
            self.state.needs["năng_lượng"] = min(100.0, self.state.needs["năng_lượng"] + 15.0)
            action_taken = "nghỉ_ngơi"
        elif self.state.needs["đói"] > 70.0:
            # Ưu tiên tìm kiếm thức ăn
            self.state.status = "tìm_kiếm"
            self.state.needs["đói"] = max(0.0, self.state.needs["đói"] - 20.0)
            action_taken = "tìm_thức_ăn"
        else:
            # Di chuyển ngẫu nhiên khám phá thế giới
            self.state.status = "di_chuyển"
            dx = rng.choice([-1, 0, 1])
            dy = rng.choice([-1, 0, 1])
            new_x = self.state.position[0] + dx
            new_y = self.state.position[1] + dy
            self.state.position = (new_x, new_y)
            action_taken = f"di_chuyển_đến_({new_x},{new_y})"

        # Ghi nhận lịch sử hành động và ký ức ngắn hạn
        self.state.action_history.append(action_taken)
        self.state.memory.append({
            "hành_động": action_taken,
            "vị_trí": self.state.position,
            "trạng_thái": self.state.status
        })
        # Giữ bộ nhớ ngắn hạn tối đa 20 sự kiện
        if len(self.state.memory) > 20:
            self.state.memory.pop(0)

        return action_taken

    def apply_external_action(self, action_type: str, payload: Optional[Dict[str, Any]] = None) -> str:
        """
        Áp dụng tác động từ bên ngoài (ví dụ: từ External Agent hoặc World Event).
        """
        payload = payload or {}
        action_taken = f"tác_động_ngoài_{action_type}"

        if action_type == "MOVE":
            target_pos = payload.get("position", self.state.position)
            self.state.position = tuple(target_pos)
            self.state.status = "di_chuyển_theo_lệnh"
        elif action_type == "REST":
            self.state.status = "nghỉ_ngơi_ép_buộc"
            self.state.needs["năng_lượng"] = min(100.0, self.state.needs["năng_lượng"] + 30.0)
        elif action_type == "SET_GOAL":
            new_goal = payload.get("goal", "mục_tiêu_mới")
            self.state.goals.append(new_goal)
            self.state.status = "thực_hiện_mục_tiêu"

        self.state.action_history.append(action_taken)
        self.state.memory.append({
            "tác_động_ngoài": action_type,
            "chi_tiết": payload,
            "vị_trí": self.state.position
        })
        return action_taken
