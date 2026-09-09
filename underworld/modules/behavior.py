"""
Mô-đun Atomic quản lý thuật toán ra quyết định hành động tự chủ của thực thể (EntityBehavior).
"""

from typing import Dict, Any, Optional
from underworld.modules.entity import EntityNeeds
from underworld.modules.spatial import SpatialSpace
from underworld.kernel.randomness import Randomness


class EntityBehavior:
    """
    Sở hữu capability ra quyết định hành động tự chủ cho thực thể dựa trên nhu cầu sinh học (EntityNeeds)
    và không gian (SpatialSpace).
    """

    def decide_and_execute(
        self,
        needs: EntityNeeds,
        spatial: SpatialSpace,
        randomness: Optional[Randomness] = None
    ) -> str:
        """
        Đưa ra quyết định và thực thi cập nhật trạng thái sinh học/vị trí.
        """
        needs.update_biology()

        action_taken = ""

        if needs.needs["năng_lượng"] < 20.0:
            needs.status = "nghỉ_ngơi"
            needs.needs["năng_lượng"] = min(100.0, needs.needs["năng_lượng"] + 15.0)
            action_taken = "nghỉ_ngơi"
        elif needs.needs["đói"] > 70.0:
            needs.status = "tìm_kiếm"
            needs.needs["đói"] = max(0.0, needs.needs["đói"] - 20.0)
            action_taken = "tìm_thức_ăn"
        else:
            needs.status = "di_chuyển"
            if randomness:
                dx = randomness.choice([-1, 0, 1])
                dy = randomness.choice([-1, 0, 1])
            else:
                import random
                dx = random.choice([-1, 0, 1])
                dy = random.choice([-1, 0, 1])

            new_pos = spatial.move_by(dx, dy)
            action_taken = f"di_chuyển_đến_({new_pos[0]},{new_pos[1]})"

        needs.record_action(action_taken, spatial.position)
        return action_taken
