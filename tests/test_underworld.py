"""
Bộ kiểm thử tự động (Unit Tests) cho Underworld v0 - PR #3.
Đảm bảo kiểm thử toàn bộ tính năng mô phỏng, Quản trị viên, chế độ vô hạn/giới hạn,
toàn vẹn ảnh chụp trạng thái và tính tái lập hạt giống ngẫu nhiên.
"""

import os
import tempfile
import unittest
from underworld.world.world import World
from underworld.human.human import Human
from underworld.engine.event_loop import EventLoop
from underworld.interface.observation import Observation
from underworld.interface.action import Action
from underworld.interface.quan_tri_vien import QuanTriVien
from underworld.data.dataset import Dataset


class DemSoLanQuanTri(QuanTriVien):
    """Lớp Quản trị viên phục vụ kiểm thử đếm số lần được gọi."""

    def __init__(self, name: str = "Admin_Test"):
        super().__init__(name=name)
        self.so_lan_goi = 0

    def tai_moi_buoc(self, trang_thai_the_gioi):
        self.so_lan_goi += 1
        return super().tai_moi_buoc(trang_thai_the_gioi)


class TestUnderworldPR3(unittest.TestCase):
    """Tập hợp các bài kiểm thử cốt lõi cho dự án Underworld v0 - PR #3."""

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

        trajectory = event_loop.chay(so_buoc=3)
        self.assertEqual(len(trajectory.steps), 3)
        self.assertEqual(world.time_step, 3)

    def test_5_human_state_changes(self):
        """5. Kiểm tra Human có thể thay đổi state theo thời gian hoặc hành động."""
        human = Human("Human_1", position=(0, 0))

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

        trajectory = event_loop.chay(so_buoc=2, trajectory_id="test_traj")
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
        trajectory = event_loop.chay(so_buoc=2)

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
        trajectory = event_loop.chay(so_buoc=5, agent_callback=None)

        self.assertEqual(len(trajectory.steps), 5)
        self.assertEqual(world.time_step, 5)

    def test_11_quan_tri_vien_duoc_goi_moi_buoc(self):
        """11. Kiểm tra Quản trị viên được gọi ở MỖI bước thời gian."""
        world = World()
        world.add_human(Human("Human_QTV"))
        event_loop = EventLoop(world)
        qtv = DemSoLanQuanTri()

        event_loop.chay(so_buoc=7, quan_tri_vien=qtv)
        self.assertEqual(qtv.so_lan_goi, 7)

    def test_12_quan_tri_vien_tac_dong_the_gioi(self):
        """12. Kiểm tra Quản trị viên có thể thay đổi môi trường và trạng thái thế giới."""
        world = World()
        qtv = QuanTriVien()
        qtv.dat_lenh_tac_dong([{
            "loai_lenh": "THAY_DOI_MOI_TRUONG",
            "key": "weather",
            "val": "sương_mù"
        }])

        event_loop = EventLoop(world)
        event_loop.chay(so_buoc=1, quan_tri_vien=qtv)

        self.assertEqual(world.environment["weather"], "sương_mù")

    def test_13_quan_tri_vien_yeu_cau_dung(self):
        """13. Kiểm tra Quản trị viên gửi lệnh dừng làm mô phỏng kết thúc sạch sẽ."""
        world = World()
        event_loop = EventLoop(world)

        class StopAfterStep3Admin(QuanTriVien):
            def tai_moi_buoc(self, trang_thai_the_gioi):
                if trang_thai_the_gioi.time_step >= 3:
                    self.yeu_cau_dung()
                return []

        admin = StopAfterStep3Admin()
        trajectory = event_loop.chay(so_buoc=None, quan_tri_vien=admin)

        # Mô phỏng bắt đầu từ t=0, dừng ở t=3
        self.assertLessEqual(len(trajectory.steps), 4)

    def test_14_chay_gioi_han_so_buoc(self):
        """14. Kiểm tra chế độ chay(so_buoc=10) kết thúc đúng sau 10 bước."""
        world = World()
        event_loop = EventLoop(world)

        trajectory = event_loop.chay(so_buoc=10)
        self.assertEqual(len(trajectory.steps), 10)
        self.assertEqual(world.time_step, 10)

    def test_15_toan_veng_anh_chup_trang_thai(self):
        """15. Kiểm tra trạng thái lịch sử (snapshot) không bị đột biến khi thế giới tiến lên."""
        world = World()
        human = Human("H_Snapshot", position=(0, 0))
        world.add_human(human)

        state_before = world.get_state()
        initial_pos = state_before.human_states["H_Snapshot"].position

        # Tiến hành 3 bước tick
        world.tick()
        world.tick()
        world.tick()

        # Kiểm tra trạng thái snapshot ban đầu vẫn giữ nguyên
        self.assertEqual(state_before.human_states["H_Snapshot"].position, initial_pos)

    def test_16_tinh_tai_lap_hat_giong_ngau_nhien(self):
        """16. Kiểm tra hai thế giới khởi tạo cùng hạt giống cho ra kết quả giống hệt nhau."""
        world1 = World(seed=999)
        world1.add_human(Human("H_Seed", position=(0, 0)))
        loop1 = EventLoop(world1)
        traj1 = loop1.chay(so_buoc=5)

        world2 = World(seed=999)
        world2.add_human(Human("H_Seed", position=(0, 0)))
        loop2 = EventLoop(world2)
        traj2 = loop2.chay(so_buoc=5)

        for step1, step2 in zip(traj1.steps, traj2.steps):
            pos1 = step1.state_after["human_states"]["H_Seed"]["position"]
            pos2 = step2.state_after["human_states"]["H_Seed"]["position"]
            self.assertEqual(pos1, pos2)


if __name__ == "__main__":
    unittest.main()
