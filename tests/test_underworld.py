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


class DemSoLanVaTimeStepQuanTri(QuanTriVien):
    """Lớp Quản trị viên phục vụ kiểm thử đếm số lần gọi và kiểm tra time_step."""

    def __init__(self, name: str = "Admin_Test"):
        super().__init__(name=name)
        self.so_lan_goi = 0
        self.danh_sach_time_step = []

    def tai_moi_buoc(self, trang_thai_the_gioi):
        self.so_lan_goi += 1
        self.danh_sach_time_step.append(trang_thai_the_gioi.time_step)
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

    def test_11_quan_tri_vien_duoc_goi_moi_buoc_voi_time_step_chinh_xac(self):
        """11. Kiểm tra Quản trị viên được gọi ở MỖI bước và nhận time_step chính xác."""
        world = World()
        world.add_human(Human("Human_QTV"))
        event_loop = EventLoop(world)
        qtv = DemSoLanVaTimeStepQuanTri()

        event_loop.chay(so_buoc=5, quan_tri_vien=qtv)
        self.assertEqual(qtv.so_lan_goi, 5)
        self.assertEqual(qtv.danh_sach_time_step, [0, 1, 2, 3, 4])

    def test_12_quan_tri_vien_thay_doi_moi_truong(self):
        """12. Kiểm tra Quản trị viên thay đổi môi trường thành công."""
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

    def test_13_quan_tri_vien_tao_su_kien(self):
        """13. Kiểm tra Quản trị viên phát lệnh TAO_SU_KIEN và sự kiện xuất hiện trong state_after."""
        world = World()
        qtv = QuanTriVien()
        qtv.dat_lenh_tac_dong([{
            "loai_lenh": "TAO_SU_KIEN",
            "chi_tiet": "Thiên thạch rơi"
        }])

        event_loop = EventLoop(world)
        trajectory = event_loop.chay(so_buoc=1, quan_tri_vien=qtv)

        state_after_events = trajectory.steps[0].state_after["events"]
        admin_events = [e for e in state_after_events if e.get("type") == "SU_KIEN_QUAN_TRI"]
        self.assertEqual(len(admin_events), 1)
        self.assertEqual(admin_events[0]["chi_tiết"], "Thiên thạch rơi")

    def test_14_quan_tri_vien_tac_dong_con_nguoi(self):
        """14. Kiểm tra Quản trị viên phát lệnh TAC_DONG_CON_NGUOI làm thay đổi Human."""
        world = World()
        human = Human("H_Target", position=(0, 0))
        human.state.needs["năng_lượng"] = 10.0  # Đặt năng lượng thấp ban đầu
        world.add_human(human)

        qtv = QuanTriVien()
        qtv.dat_lenh_tac_dong([{
            "loai_lenh": "TAC_DONG_CON_NGUOI",
            "target_id": "H_Target",
            "action_type": "REST",
            "payload": {"reason": "Nghỉ ngơi theo lệnh Quản trị viên"}
        }])

        event_loop = EventLoop(world)
        event_loop.chay(so_buoc=1, quan_tri_vien=qtv)

        # Ban đầu 10.0 -> lệnh REST +30 = 40.0 -> tick trừ 2.0 = 38.0
        self.assertIn("tác_động_ngoài_REST", human.state.action_history)
        self.assertEqual(human.state.needs["năng_lượng"], 38.0)

    def test_15_quan_tri_vien_dung_bang_loai_lenh(self):
        """15. Kiểm tra Quản trị viên phát lệnh YEU_CAU_DUNG qua danh sách lệnh và mô phỏng dừng."""
        world = World()
        qtv = QuanTriVien()
        qtv.dat_lenh_tac_dong([{
            "loai_lenh": "YEU_CAU_DUNG"
        }])

        event_loop = EventLoop(world)
        trajectory = event_loop.chay(so_buoc=None, quan_tri_vien=qtv)

        self.assertEqual(len(trajectory.steps), 0)
        self.assertEqual(world.time_step, 0)
        self.assertTrue(qtv.dang_yeu_cau_dung())

    def test_16_quan_tri_vien_yeu_cau_dung_chinh_xac(self):
        """16. Kiểm tra Quản trị viên yêu cầu dừng ở time_step=3 kết thúc với chính xác 3 bước."""
        world = World()
        world.add_human(Human("H_Stop"))
        event_loop = EventLoop(world)

        class StopAtStep3Admin(QuanTriVien):
            def tai_moi_buoc(self, trang_thai_the_gioi):
                if trang_thai_the_gioi.time_step == 3:
                    self.yeu_cau_dung()
                return super().tai_moi_buoc(trang_thai_the_gioi)

        admin = StopAtStep3Admin()
        trajectory = event_loop.chay(so_buoc=None, quan_tri_vien=admin)

        self.assertEqual(len(trajectory.steps), 3)
        self.assertEqual(world.time_step, 3)

    def test_17_chay_gioi_han_so_buoc(self):
        """17. Kiểm tra chế độ chay(so_buoc=10) kết thúc đúng sau 10 bước."""
        world = World()
        event_loop = EventLoop(world)

        trajectory = event_loop.chay(so_buoc=10)
        self.assertEqual(len(trajectory.steps), 10)
        self.assertEqual(world.time_step, 10)

    def test_18_toan_veng_anh_chup_trang_thai_sau(self):
        """18. Kiểm tra trạng thái snapshot độc lập hoàn toàn ở các cấu trúc dữ liệu lồng nhau."""
        world = World()
        human = Human("H_Snapshot", position=(0, 0))
        world.add_human(human)

        state_before = world.get_state()
        initial_needs = dict(state_before.human_states["H_Snapshot"].needs)
        initial_resources = dict(state_before.environment["resources"])

        # Tiến hành 3 bước tick làm biến đổi năng lượng/nhu cầu/môi trường
        world.tick()
        world.tick()
        world.tick()

        # Kiểm tra dữ liệu lồng nhau trong snapshot ban đầu hoàn toàn không bị ảnh hưởng
        self.assertEqual(state_before.human_states["H_Snapshot"].needs, initial_needs)
        self.assertEqual(state_before.environment["resources"], initial_resources)

    def test_19_tinh_tai_lap_hat_giong_ngau_nhien_manh(self):
        """19. Kiểm tra hai thế giới cùng hạt giống tái lập 100% toàn bộ Trajectory."""
        world1 = World(seed=12345)
        world1.add_human(Human("H_Seed", position=(0, 0)))
        loop1 = EventLoop(world1)
        traj1 = loop1.chay(so_buoc=5)

        world2 = World(seed=12345)
        world2.add_human(Human("H_Seed", position=(0, 0)))
        loop2 = EventLoop(world2)
        traj2 = loop2.chay(so_buoc=5)

        for s1, s2 in zip(traj1.steps, traj2.steps):
            self.assertEqual(s1.step, s2.step)
            self.assertEqual(s1.state_after["human_states"]["H_Seed"]["position"],
                             s2.state_after["human_states"]["H_Seed"]["position"])
            self.assertEqual(s1.state_after["human_states"]["H_Seed"]["needs"],
                             s2.state_after["human_states"]["H_Seed"]["needs"])
            self.assertEqual(s1.state_after["human_states"]["H_Seed"]["action_history"],
                             s2.state_after["human_states"]["H_Seed"]["action_history"])

    def test_20_hat_giong_khac_nhau_sinh_ket_qua_khac(self):
        """20. Kiểm tra hai thế giới với hạt giống khác nhau tạo ra quỹ đạo khác nhau."""
        world1 = World(seed=111)
        world1.add_human(Human("H_Diff", position=(0, 0)))
        traj1 = EventLoop(world1).chay(so_buoc=10)

        world2 = World(seed=999)
        world2.add_human(Human("H_Diff", position=(0, 0)))
        traj2 = EventLoop(world2).chay(so_buoc=10)

        positions_1 = [s.state_after["human_states"]["H_Diff"]["position"] for s in traj1.steps]
        positions_2 = [s.state_after["human_states"]["H_Diff"]["position"] for s in traj2.steps]

        self.assertNotEqual(positions_1, positions_2)


if __name__ == "__main__":
    unittest.main()
