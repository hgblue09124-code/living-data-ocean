"""
Bộ kiểm thử tự động (Unit Tests) cho Underworld v0.
Đảm bảo đáp ứng đầy đủ 10 tiêu chí bắt buộc trong yêu cầu bài tập.
"""

import os
import tempfile
import unittest
from underworld.world.world import World
from underworld.human.human import Human
from underworld.engine.event_loop import EventLoop
from underworld.interface.observation import Observation
from underworld.interface.action import Action
from underworld.data.dataset import Dataset


class TestUnderworld(unittest.TestCase):
    """Tập hợp 10 bài kiểm thử cốt lõi cho hệ thống Underworld v0."""

    def test_1_world_initialization(self):
        """1. Kiểm tra World khởi tạo được thành công."""
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

        # Cho human di chuyển / giảm năng lượng
        human.state.needs["năng_lượng"] = 10.0  # Giảm xuống dưới 20
        action = human.step()

        self.assertEqual(action, "nghỉ_ngơi")
        self.assertEqual(human.state.status, "nghỉ_ngơi")
        self.assertGreater(human.state.needs["năng_lượng"], 10.0)

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
        self.assertEqual(human.state.position, (9, 9))
        self.assertEqual(human.state.status, "di_chuyển_theo_lệnh")

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

    def test_10_autonomous_simulation_without_external_agent(self):
        """10. Kiểm tra Simulation vẫn tự chạy hoàn hảo khi KHÔNG có External Agent."""
        world = World()
        world.add_human(Human("Auto_1", position=(0, 0)))
        world.add_human(Human("Auto_2", position=(10, 10)))

        event_loop = EventLoop(world)
        # Chạy mà KHÔNG truyền agent_callback
        trajectory = event_loop.run(steps=5, agent_callback=None)

        self.assertEqual(len(trajectory.steps), 5)
        self.assertEqual(world.time_step, 5)
        for step in trajectory.steps:
            self.assertIsNone(step.action)


if __name__ == "__main__":
    unittest.main()
