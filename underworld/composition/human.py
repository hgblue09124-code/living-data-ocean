"""
Mô-đun Composition hợp thành thực thể Human từ các Atomic Modules.
"""

import copy
import random
from typing import Dict, Any, Optional, Tuple
from underworld.kernel.identity import EntityIdentity
from underworld.modules.spatial import SpatialSpace
from underworld.modules.entity import EntityNeeds
from underworld.modules.behavior import EntityBehavior
from underworld.composition.state import HumanState


class Human:
    """
    Thực thể Human được tạo nên từ việc Composition (tổng hợp) các Atomic Modules:
    - EntityIdentity: Quản lý định danh
    - SpatialSpace: Quản lý vị trí không gian
    - EntityNeeds: Quản lý thuộc tính nhu cầu sinh học và ký ức
    - EntityBehavior: Quản lý thuật toán ra quyết định hành động tự chủ
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
        self.behavior = EntityBehavior()

    @property
    def state(self) -> HumanState:
        """Property hỗ trợ truy cập tương thích với trạng thái HumanState."""
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
        Ủy quyền ra quyết định hành động cho EntityBehavior atomic module.
        """
        rng = (context and context.get("random")) or None
        return self.behavior.decide_and_execute(
            needs=self.needs,
            spatial=self.spatial,
            randomness=rng
        )

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
