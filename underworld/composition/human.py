"""
Mô-đun Composition hợp thành thực thể Human từ các Atomic Modules.
"""

import copy
import random
from typing import Dict, Any, Optional, Tuple
from underworld.kernel.identity import EntityIdentity
from underworld.modules.spatial import SpatialSpace
from underworld.modules.entity import EntityNeeds
from underworld.human.state import HumanState


class Human:
    """
    Thực thể Human được tạo nên từ việc Composition (tổng hợp) 3 Atomic Modules:
    - EntityIdentity: Quản lý định danh
    - SpatialSpace: Quản lý vị trí không gian
    - EntityNeeds: Quản lý các thuộc tính nhu cầu nội tại và ký ức
    """

    def __init__(
        self,
        human_id: str,
        position: Tuple[int, int] = (0, 0),
        status: str = "thong_dong",
        needs: Optional[Dict[str, float]] = None,
        goals: Optional[list] = None
    ):
        """Khởi tạo một thực thể Human thông qua Composition."""
        self.identity = EntityIdentity(human_id)
        self.spatial = SpatialSpace(position=position)
        self.needs = EntityNeeds(status=status, needs=needs, goals=goals)

    @property
    def state(self) -> HumanState:
        """Property hỗ trợ truy cập tương thích với phiên bản cũ."""
        return HumanState(
            id=self.identity.id,
            position=self.spatial.position,
            status=self.needs.status,
            needs=self.needs.needs,
            goals=self.needs.goals,
            memory=self.needs.memory,
            action_history=self.needs.action_history
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
        rng = (context and context.get("random")) or random

        # Ủy quyền cập nhật nhu cầu sinh học cho EntityNeeds
        self.needs.update_biology()

        action_taken = ""

        if self.needs.needs["năng_lượng"] < 20.0:
            self.needs.status = "nghỉ_ngơi"
            self.needs.needs["năng_lượng"] = min(100.0, self.needs.needs["năng_lượng"] + 15.0)
            action_taken = "nghỉ_ngơi"
        elif self.needs.needs["đói"] > 70.0:
            self.needs.status = "tìm_kiếm"
            self.needs.needs["đói"] = max(0.0, self.needs.needs["đói"] - 20.0)
            action_taken = "tìm_thức_ăn"
        else:
            self.needs.status = "di_chuyển"
            dx = rng.choice([-1, 0, 1])
            dy = rng.choice([-1, 0, 1])
            new_pos = self.spatial.move_by(dx, dy)
            action_taken = f"di_chuyển_đến_({new_pos[0]},{new_pos[1]})"

        # Ủy quyền ghi nhận lịch sử cho EntityNeeds
        self.needs.record_action(action_taken, self.spatial.position)
        return action_taken

    def apply_external_action(self, action_type: str, payload: Optional[Dict[str, Any]] = None) -> str:
        """
        Áp dụng tác động từ bên ngoài (từ External Agent hoặc AdministratorCommand).
        """
        payload = payload or {}
        action_taken = f"tác_động_ngoài_{action_type}"

        if action_type == "MOVE":
            target_pos = payload.get("position", self.spatial.position)
            self.spatial.set_position(target_pos)
            self.needs.status = "di_chuyển_theo_lệnh"
        elif action_type == "REST":
            self.needs.status = "nghỉ_ngơi_ép_buộc"
            self.needs.needs["năng_lượng"] = min(100.0, self.needs.needs["năng_lượng"] + 30.0)
        elif action_type == "SET_GOAL":
            new_goal = payload.get("goal", "mục_tiêu_mới")
            self.needs.goals.append(new_goal)
            self.needs.status = "thực_hiện_mục_tiêu"

        self.needs.record_action(action_taken, self.spatial.position)
        return action_taken
