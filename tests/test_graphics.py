"""
Các bài kiểm thử tự động cho World Program, World Graphics và UI Program Composition.
"""

import unittest
from typing import Dict, Any

from underworld.composition.world import World
from underworld.composition.world_program import WorldProgram
from underworld.graphics.world_graphics import WorldGraphics
from underworld.graphics.ui_program import UIProgram
from underworld.modules.ui.base import UIModule
from underworld.modules.ui import (
    WorldStateViewModule,
    EntityViewModule,
    EventViewModule,
    TimelineViewModule,
    SimulationControlViewModule,
)
from underworld.modules.spatial import SpatialSpace
from underworld.modules.environment import EnvironmentState


class DummyConfigModule:
    """Module bổ trợ cấu hình giả lập để kiểm thử tác động của active_modules lên WorldProgram."""
    def __init__(self, bounds=(200, 200), seed=999, initial_humans_count=5):
        self.module_id = "mod_dummy_config"
        self.bounds = bounds
        self.seed = seed
        self.initial_humans_count = initial_humans_count


class TestWorldGraphicsAndUIProgram(unittest.TestCase):
    """Bộ kiểm thử khả năng chọn lựa, sắp xếp và tổng hợp UI Program từ World Graphics."""

    def setUp(self):
        self.ui_state_view = WorldStateViewModule()
        self.ui_entity_view = EntityViewModule()
        self.ui_event_view = EventViewModule()
        self.ui_timeline_view = TimelineViewModule()
        self.ui_control_view = SimulationControlViewModule()

        self.domain_mod_1 = SpatialSpace()
        self.domain_mod_2 = EnvironmentState()

        # Hệ sinh thái hỗn hợp giữa Domain Modules và UI Modules
        self.ecosystem = [
            self.domain_mod_1,
            self.ui_state_view,
            self.domain_mod_2,
            self.ui_entity_view,
            self.ui_event_view,
            self.ui_timeline_view,
            self.ui_control_view
        ]

        self.graphics = WorldGraphics(available_modules=self.ecosystem)

    def test_filter_ui_modules(self):
        """Xác minh WorldGraphics lọc chính xác chỉ các UI Modules."""
        filtered = self.graphics.filter_ui_modules(self.ecosystem)
        self.assertEqual(len(filtered), 5)
        for mod in filtered:
            self.assertTrue(isinstance(mod, UIModule) or getattr(mod, "is_ui_module", False))

    def test_order_ui_modules(self):
        """Xác minh WorldGraphics sắp xếp UI Modules theo đúng thứ tự layout mong muốn."""
        filtered = self.graphics.filter_ui_modules(self.ecosystem)
        custom_order = [
            "ui_timeline_view",
            "ui_simulation_control_view",
            "ui_world_state_view"
        ]
        ordered = self.graphics.order_ui_modules(filtered, layout_order=custom_order)

        ordered_ids = [m.module_id for m in ordered]
        self.assertEqual(ordered_ids[0], "ui_timeline_view")
        self.assertEqual(ordered_ids[1], "ui_simulation_control_view")
        self.assertEqual(ordered_ids[2], "ui_world_state_view")
        self.assertEqual(len(ordered), 5)

    def test_empty_and_single_ui_module_composition(self):
        """Xác minh WorldGraphics xử lý chính xác tập UI modules rỗng hoặc chỉ có 1 module."""
        empty_graphics = WorldGraphics(available_modules=[self.domain_mod_1])
        ui_prog_empty = empty_graphics.compose_ui_program()
        self.assertEqual(len(ui_prog_empty.ui_modules), 0)

        single_graphics = WorldGraphics(available_modules=[self.ui_state_view])
        ui_prog_single = single_graphics.compose_ui_program()
        self.assertEqual(len(ui_prog_single.ui_modules), 1)
        self.assertEqual(ui_prog_single.ui_modules[0].module_id, "ui_world_state_view")

    def test_compose_different_ui_programs(self):
        """Xác minh cùng một hệ sinh thái Modules có thể tạo ra các UI Programs khác nhau."""
        layout_a = ["ui_world_state_view", "ui_simulation_control_view"]
        layout_b = ["ui_entity_view", "ui_timeline_view", "ui_event_view"]

        ui_program_a = self.graphics.compose_ui_program(layout_order=layout_a, title="Program A")
        ui_program_b = self.graphics.compose_ui_program(layout_order=layout_b, title="Program B")

        ids_a = [m.module_id for m in ui_program_a.ui_modules]
        ids_b = [m.module_id for m in ui_program_b.ui_modules]

        self.assertEqual(ids_a[0], "ui_world_state_view")
        self.assertEqual(ids_a[1], "ui_simulation_control_view")

        self.assertEqual(ids_b[0], "ui_entity_view")
        self.assertEqual(ids_b[1], "ui_timeline_view")
        self.assertEqual(ids_b[2], "ui_event_view")

    def test_world_graphics_does_not_own_simulation_state(self):
        """Xác minh WorldGraphics không nắm giữ hay làm biến đổi trạng thái mô phỏng."""
        self.assertFalse(hasattr(self.graphics, "time_step"))
        self.assertFalse(hasattr(self.graphics, "humans"))
        self.assertFalse(hasattr(self.graphics, "world_state"))

    def test_world_program_module_selection_and_influences(self):
        """Xác minh WorldProgram thực sự chọn lựa và cho phép Modules ảnh hưởng tới chương trình thực thi."""
        dummy_mod = DummyConfigModule(bounds=(300, 300), seed=888, initial_humans_count=4)
        extended_ecosystem = self.ecosystem + [dummy_mod]

        program = WorldProgram.assemble(
            available_modules=extended_ecosystem,
            world_seed=123,
            num_humans=2
        )
        st = program.get_state()

        self.assertEqual(st["time_step"], 0)
        self.assertEqual(len(st["human_states"]), 4)  # Bị ảnh hưởng bởi dummy_mod
        self.assertEqual(st["environment"]["bounds"], [300, 300])  # Bị ảnh hưởng bởi dummy_mod

        after_st = program.run_step()
        self.assertEqual(after_st["time_step"], 1)


if __name__ == "__main__":
    unittest.main()
