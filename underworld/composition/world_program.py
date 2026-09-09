"""WorldProgram — Chương trình thực thi mô phỏng được lắp ghép từ Modules.

World Program chịu trách nhiệm chọn lựa, sắp xếp và tổng hợp các Modules thành một
chương trình mô phỏng hoàn chỉnh có thể vận hành trên nền tảng (substrate) World.
"""

from typing import List, Any, Optional, Dict
from underworld.composition.world import World
from underworld.composition.human import Human
from underworld.composition.state import WorldState
from underworld.runtime.event_loop import EventLoop


class WorldProgram:
    """Chương trình mô phỏng thực thi (Executable Program) được tổng hợp từ Modules."""

    def __init__(
        self,
        world: World,
        event_loop: EventLoop,
        active_modules: Optional[List[Any]] = None
    ):
        """Khởi tạo World Program.

        Args:
            world: Nền tảng thực thi World (substrate).
            event_loop: Động cơ điều phối vòng lặp mô phỏng.
            active_modules: Danh sách các modules được chọn tham gia chương trình này.
        """
        self.world = world
        self.event_loop = event_loop
        self.active_modules = active_modules or []

    @classmethod
    def assemble(
        cls,
        available_modules: List[Any],
        module_selector: Optional[List[str]] = None,
        world_seed: int = 42,
        num_humans: int = 3
    ) -> "WorldProgram":
        """Tổng hợp một World Program từ hệ sinh thái Modules sẵn có.

        Args:
            available_modules: Tập hợp toàn bộ Modules có sẵn.
            module_selector: Danh sách ID các modules cần lọc sử dụng (nếu None, dùng tất cả).
            world_seed: Hạt giống ngẫu nhiên cho thế giới.
            num_humans: Số lượng con người ban đầu.

        Returns:
            Một thể hiện WorldProgram sẵn sàng thực thi.
        """
        selected_modules = []
        for mod in available_modules:
            mod_id = getattr(mod, "module_id", getattr(mod, "id", str(mod)))
            if module_selector is None or mod_id in module_selector:
                selected_modules.append(mod)

        world = World(seed=world_seed)
        for i in range(1, num_humans + 1):
            h_id = f"Human_{i:03d}"
            h = Human(human_id=h_id, position=(i * 2, i * 2))
            world.add_human(h)

        event_loop = EventLoop(world=world)

        return cls(world=world, event_loop=event_loop, active_modules=selected_modules)

    def run_step(self) -> Dict[str, Any]:
        """Thực thi một bước (tick) mô phỏng trong chương trình.

        Returns:
            Snapshot trạng thái thế giới (dict) sau khi tick.
        """
        self.event_loop.run(steps=1)
        st = self.world.get_state()
        return st.to_dict() if hasattr(st, "to_dict") else st

    def get_state(self) -> Dict[str, Any]:
        """Lấy snapshot trạng thái thế giới hiện tại dạng dict."""
        st = self.world.get_state()
        return st.to_dict() if hasattr(st, "to_dict") else st
