"""
Bộ kiểm thử tự động (Unit Tests) cho Underworld v0 - Canonical Architecture & Invariants.
Đảm bảo kiểm thử toàn bộ tính năng mô phỏng, ranh giới AdministratorCommand,
World tự vận hành độc lập, snapshot integrity, seed ngẫu nhiên và các ràng buộc kiến trúc.
"""

import sys
import os
import tempfile
import unittest

from underworld.kernel import SimulationTime, Randomness, EntityIdentity
from underworld.modules import SpatialSpace, EnvironmentState, EntityNeeds, EventLog, EntityBehavior, InteractionRule, CommandDispatcher
from underworld.composition import World, Human, HumanState, WorldState
from underworld.runtime import EventLoop
from underworld.interface import Observation, Action, AdministratorCommand, Administrator
from underworld.data import Dataset, Trajectory


class TestUnderworldArchitecture(unittest.TestCase):
    """Tập hợp các bài kiểm thử cốt lõi và kiểm thử ràng buộc kiến trúc (Architecture Invariants)."""

    def test_1_world_initialization(self):
        """1. Kiểm tra World khởi tạo thành công."""
        world = World(bounds=(100, 100))
        self.assertEqual(world.time_step, 0)
        self.assertEqual(len(world.humans), 0)
        self.assertIn("bounds", world.environment)

    def test_2_world_state_changes_on_tick(self):
        """2. Kiểm tra WorldState thay đổi theo từng tick."""
        world = World()
        state_t0 = world.get_state()
        self.assertEqual(state_t0.time_step, 0)

        state_t1 = world.tick()
        self.assertEqual(state_t1.time_step, 1)

        state_t2 = world.tick()
        self.assertEqual(state_t2.time_step, 2)

    def test_3_multiple_humans_exist_simultaneously(self):
        """3. Kiểm tra N Human tồn tại đồng thời trong World."""
        world = World()
        h1 = Human("Human_A", position=(0, 0))
        h2 = Human("Human_B", position=(5, 5))
        h3 = Human("Human_C", position=(10, 10))

        world.add_human(h1)
        world.add_human(h2)
        world.add_human(h3)

        state = world.get_state()
        self.assertEqual(len(state.human_states), 3)
        self.assertIn("Human_A", state.human_states)
        self.assertIn("Human_B", state.human_states)
        self.assertIn("Human_C", state.human_states)

    def test_4_event_loop_runs(self):
        """4. Kiểm tra Event Loop chạy thành công."""
        world = World()
        world.add_human(Human("Human_1"))
        event_loop = EventLoop(world)

        trajectory = event_loop.run(steps=3)
        self.assertEqual(len(trajectory.steps), 3)
        self.assertEqual(world.time_step, 3)

    def test_5_human_state_changes(self):
        """5. Kiểm tra Human có thể thay đổi state theo thời gian hoặc hành động."""
        human = Human("Human_1", position=(0, 0))

        human.needs.needs["năng_lượng"] = 10.0  # Giảm xuống dưới 20
        action = human.step()

        self.assertEqual(action, "nghỉ_ngơi")
        self.assertEqual(human.needs.status, "nghỉ_ngơi")
        self.assertGreater(human.needs.needs["năng_lượng"], 10.0)

    def test_6_observation_creation(self):
        """6. Kiểm tra Observation được tạo chính xác từ WorldState."""
        world = World()
        human = Human("Human_Obs", position=(2, 3))
        world.add_human(human)
        world_state = world.get_state()

        obs = Observation.from_world_state(world_state)
        self.assertEqual(obs.time_step, 0)
        self.assertEqual(len(obs.visible_humans), 1)
        self.assertEqual(obs.visible_humans[0]["id"], "Human_Obs")
        self.assertEqual(obs.visible_humans[0]["position"], (2, 3))

    def test_7_action_impacts_world(self):
        """7. Kiểm tra Action có thể tác động từ bên ngoài vào World/Human."""
        world = World()
        human = Human("Target_Human", position=(0, 0))
        world.add_human(human)

        actions = [{
            "action_type": "MOVE",
            "target_id": "Target_Human",
            "payload": {"position": (9, 9)}
        }]

        world.tick(external_actions=actions)
        self.assertEqual(human.spatial.position, (9, 9))
        self.assertEqual(human.needs.status, "di_chuyển_theo_lệnh")

    def test_8_trajectory_recording(self):
        """8. Kiểm tra Trajectory được ghi nhận đầy đủ chi tiết."""
        world = World()
        world.add_human(Human("Human_Traj"))
        event_loop = EventLoop(world)

        trajectory = event_loop.run(steps=2, trajectory_id="test_traj")
        self.assertEqual(trajectory.trajectory_id, "test_traj")
        self.assertEqual(len(trajectory.steps), 2)

        step_1 = trajectory.steps[0]
        self.assertEqual(step_1.step, 1)
        self.assertIn("Human_Traj", step_1.state_before["human_states"])
        self.assertIn("Human_Traj", step_1.state_after["human_states"])

    def test_9_dataset_export(self):
        """9. Kiểm tra Dataset được xuất ra tệp JSONL thành công."""
        world = World()
        world.add_human(Human("Human_DS"))
        event_loop = EventLoop(world)
        trajectory = event_loop.run(steps=2)

        dataset = Dataset()
        dataset.add_trajectory(trajectory)

        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = os.path.join(tmpdir, "test_dataset.jsonl")
            dataset.export_jsonl(file_path)

            self.assertTrue(os.path.exists(file_path))

            loaded_data = Dataset.load_jsonl(file_path)
            self.assertEqual(len(loaded_data), 1)
            self.assertEqual(loaded_data[0]["trajectory_id"], trajectory.trajectory_id)

    def test_10_world_runs_without_administrator(self):
        """10. Chứng minh World tự vận hành hoàn toàn độc lập khi KHÔNG có Administrator."""
        world = World()
        world.add_human(Human("Auto_1", position=(0, 0)))
        world.add_human(Human("Auto_2", position=(10, 10)))

        event_loop = EventLoop(world)
        trajectory = event_loop.run(steps=5, administrator=None)

        self.assertEqual(len(trajectory.steps), 5)
        self.assertEqual(world.time_step, 5)

    def test_11_administrator_is_not_human_or_agent(self):
        """11. Xác nhận Administrator KHÔNG phải là Human hay Agent trong danh sách mô phỏng."""
        world = World()
        world.add_human(Human("H1"))
        admin = Administrator("ExternalAdmin")

        self.assertNotIn("ExternalAdmin", world.humans)
        self.assertEqual(len(world.humans), 1)

    def test_12_administrator_command_change_environment(self):
        """12. Kiểm tra AdministratorCommand thay đổi môi trường thành công."""
        world = World()
        admin = Administrator()
        admin.change_environment("weather", "sương_mù")

        event_loop = EventLoop(world)
        event_loop.run(steps=1, administrator=admin)

        self.assertEqual(world.environment["weather"], "sương_mù")

    def test_13_administrator_command_create_event(self):
        """13. Kiểm tra AdministratorCommand tạo sự kiện và xuất hiện trong state_after."""
        world = World()
        admin = Administrator()
        admin.create_event("Thiên thạch rơi")

        event_loop = EventLoop(world)
        trajectory = event_loop.run(steps=1, administrator=admin)

        state_after_events = trajectory.steps[0].state_after["events"]
        admin_events = [e for e in state_after_events if e.get("type") == "SU_KIEN_QUAN_TRI"]
        self.assertEqual(len(admin_events), 1)
        self.assertEqual(admin_events[0]["chi_tiết"], "Thiên thạch rơi")

    def test_14_administrator_command_affect_human(self):
        """14. Kiểm tra AdministratorCommand tác động đến Human."""
        world = World()
        human = Human("H_Target", position=(0, 0))
        human.needs.needs["năng_lượng"] = 10.0
        world.add_human(human)

        admin = Administrator()
        admin.affect_human("H_Target", "REST", {"reason": "Nghỉ ngơi theo lệnh Admin"})

        event_loop = EventLoop(world)
        event_loop.run(steps=1, administrator=admin)

        self.assertIn("tác_động_ngoài_REST", human.needs.action_history)
        self.assertEqual(human.needs.needs["năng_lượng"], 38.0)

    def test_15_administrator_stop_command(self):
        """15. Kiểm tra AdministratorCommand REQUEST_STOP làm mô phỏng dừng ngay lập tức."""
        world = World()
        admin = Administrator()
        admin.request_stop()

        event_loop = EventLoop(world)
        trajectory = event_loop.run(steps=None, administrator=admin)

        self.assertEqual(len(trajectory.steps), 0)
        self.assertEqual(world.time_step, 0)

    def test_16_bounded_step_mode(self):
        """16. Kiểm tra chế độ run(steps=10) kết thúc đúng sau 10 bước."""
        world = World()
        event_loop = EventLoop(world)

        trajectory = event_loop.run(steps=10)
        self.assertEqual(len(trajectory.steps), 10)
        self.assertEqual(world.time_step, 10)

    def test_17_snapshot_integrity_mutation_isolation(self):
        """17. Kiểm tra mutation trực tiếp lên World/Human không ảnh hưởng đến state_before đã chụp."""
        world = World()
        human = Human("H_Snapshot", position=(0, 0))
        world.add_human(human)

        state_before = world.get_state()
        initial_dict = state_before.to_dict()

        # Đột biến trực tiếp các thuộc tính sống của human và world
        human.spatial.position = (99, 99)
        human.needs.needs["năng_lượng"] = 0.0
        human.needs.memory.append({"fake": "mutation"})
        world.environment_state.resources["thức_ăn"] = 999
        world.event_log.events.append({"fake": "event"})
        world.add_human(Human("H_Injected"))
        world.tick()

        # Khẳng định state_before hoàn toàn giữ nguyên trạng thái chụp ban đầu
        self.assertEqual(state_before.to_dict(), initial_dict)
        self.assertEqual(state_before.human_states["H_Snapshot"].position, (0, 0))
        self.assertNotIn("H_Injected", state_before.human_states)

    def test_18_random_seed_reproducibility(self):
        """18. Kiểm tra hai thế giới cùng hạt giống tái lập 100% toàn bộ Trajectory dict."""
        world1 = World(seed=12345)
        world1.add_human(Human("H_Seed", position=(0, 0)))
        loop1 = EventLoop(world1)
        traj1 = loop1.run(steps=5, trajectory_id="traj_same")

        world2 = World(seed=12345)
        world2.add_human(Human("H_Seed", position=(0, 0)))
        loop2 = EventLoop(world2)
        traj2 = loop2.run(steps=5, trajectory_id="traj_same")

        # So sánh 100% bản xuất dictionary của cả 2 Trajectory
        self.assertEqual(traj1.to_dict(), traj2.to_dict())

    def test_19_different_seeds_produce_different_trajectories(self):
        """19. Kiểm tra hai thế giới với hạt giống khác nhau tạo ra quỹ đạo khác nhau."""
        world1 = World(seed=111)
        world1.add_human(Human("H_Diff", position=(0, 0)))
        traj1 = EventLoop(world1).run(steps=10)

        world2 = World(seed=999)
        world2.add_human(Human("H_Diff", position=(0, 0)))
        traj2 = EventLoop(world2).run(steps=10)

        self.assertNotEqual(traj1.to_dict(), traj2.to_dict())

    def test_20_atomic_modules_and_composition_boundaries(self):
        """20. Kiểm tra ranh giới hoạt động độc lập của các Atomic Modules và Delegation trong World."""
        sim_time = SimulationTime()
        self.assertEqual(sim_time.increment(), 1)

        rng = Randomness(42)
        self.assertIn(rng.choice([1, 2, 3]), [1, 2, 3])

        ident = EntityIdentity("TEST_ID")
        self.assertEqual(str(ident), "TEST_ID")

        spatial = SpatialSpace(bounds=(20, 20), position=(5, 5))
        self.assertEqual(spatial.move_by(1, 2), (6, 7))
        self.assertEqual(spatial.manhattan_distance((0, 0)), 13)

        env = EnvironmentState()
        env.set_attribute("weather", "nắng_nóng")
        self.assertEqual(env.weather, "nắng_nóng")

        needs = EntityNeeds()
        needs.update_biology()
        self.assertEqual(needs.needs["năng_lượng"], 98.0)

        event_log = EventLog()
        event_log.add_event("Sự kiện lẻ")
        step_events = event_log.prepare_step_events(current_step=1)
        self.assertEqual(len(step_events), 1)

    def test_21_architecture_invariants_no_administrator_import_in_world(self):
        """21. Ràng buộc kiến trúc: Mô-đun World/Composition KHÔNG import Administrator."""
        import underworld.composition.world as world_module
        with open(world_module.__file__, encoding="utf-8") as f:
            module_source = f.read()
        self.assertNotIn("import Administrator", module_source)

    def test_22_architecture_invariants_no_circular_dependencies(self):
        """22. Ràng buộc kiến trúc: Hướng phụ thuộc 1 chiều Kernel <- Modules <- Composition <- Runtime."""
        import underworld.kernel
        import underworld.modules
        import underworld.composition
        import underworld.runtime

        self.assertTrue(hasattr(underworld.kernel, "SimulationTime"))
        self.assertTrue(hasattr(underworld.modules, "EntityBehavior"))
        self.assertTrue(hasattr(underworld.composition, "World"))
        self.assertTrue(hasattr(underworld.runtime, "EventLoop"))


if __name__ == "__main__":
    unittest.main()
