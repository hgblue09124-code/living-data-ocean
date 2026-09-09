"""
Bài kiểm thử tự động cho Web UI Presentation Layer, REST API Endpoints, Auto-Run Ticker và Snapshot Integrity.
"""

import unittest
import json
import threading
import urllib.request
import urllib.parse
import time
from typing import Dict, Any

from underworld.composition.world import World
from underworld.composition.world_program import WorldProgram
from underworld.graphics.world_graphics import WorldGraphics
from underworld.graphics.ui_program import UIProgram
from underworld.graphics.web_server import start_web_server, UnderworldWebHandler
from underworld.interface.administrator import Administrator
from underworld.modules.spatial import SpatialSpace
from underworld.modules.environment import EnvironmentState
from underworld.modules.ui import (
    WorldStateViewModule,
    EntityViewModule,
    EventViewModule,
    TimelineViewModule,
    SimulationControlViewModule,
)


class TestWebUIAndSnapshotIntegrity(unittest.TestCase):
    """Bộ kiểm thử cho Web UI Layer và tính bất biến của Snapshot Integrity."""

    def setUp(self):
        self.ecosystem = [
            SpatialSpace(),
            EnvironmentState(),
            WorldStateViewModule(),
            EntityViewModule(),
            EventViewModule(),
            TimelineViewModule(),
            SimulationControlViewModule()
        ]
        self.world_program = WorldProgram.assemble(
            available_modules=self.ecosystem,
            world_seed=99,
            num_humans=3
        )
        self.world_graphics = WorldGraphics(available_modules=self.ecosystem)
        self.ui_program = self.world_graphics.compose_ui_program(
            layout_order=[
                "ui_world_state_view",
                "ui_simulation_control_view",
                "ui_entity_view",
                "ui_event_view",
                "ui_timeline_view"
            ],
            title="Test Web UI"
        )
        self.admin = Administrator(name="TestAdmin")

    def test_snapshot_integrity_deep_copy(self):
        """Xác minh get_state() trả về snapshot bất biến không bị ảnh hưởng khi world tick tiếp."""
        st_before = self.world_program.get_state()
        tick_before = st_before["time_step"]

        # Tick thế giới 3 bước
        for _ in range(3):
            self.world_program.run_step()

        st_after = self.world_program.get_state()

        # Kiểm tra snapshot lịch sử ban đầu không bị biến đổi
        self.assertEqual(st_before["time_step"], tick_before)
        self.assertEqual(st_after["time_step"], tick_before + 3)

    def test_web_presentation_payload_generation(self):
        """Xác minh UIProgram tạo Web Presentation Payload chính xác từ state."""
        st = self.world_program.get_state()
        payload = self.ui_program.generate_web_presentation(st)

        self.assertEqual(payload["title"], "Test Web UI")
        self.assertEqual(payload["modules_count"], 5)
        self.assertEqual(len(payload["modules"]), 5)

        mod_types = [m["type"] for m in payload["modules"]]
        self.assertIn("world_state_summary", mod_types)
        self.assertIn("control_panel", mod_types)
        self.assertIn("entity_table", mod_types)
        self.assertIn("event_list", mod_types)
        self.assertIn("timeline_log", mod_types)

    def test_web_server_endpoints_and_new_commands(self):
        """Xác minh các REST Endpoints (/api/state, /api/step, /api/command, /api/auto_toggle) hoạt động chuẩn xác."""
        server = start_web_server(
            world_program=self.world_program,
            ui_program=self.ui_program,
            admin=self.admin,
            host="127.0.0.1",
            port=8889
        )
        server_thread = threading.Thread(target=server.serve_forever)
        server_thread.daemon = True
        server_thread.start()

        time.sleep(0.1)

        try:
            # 1. Test GET /api/state
            req = urllib.request.urlopen("http://127.0.0.1:8889/api/state")
            self.assertEqual(req.status, 200)
            data = json.loads(req.read().decode("utf-8"))
            self.assertEqual(data["title"], "Test Web UI")

            # 2. Test GET /api/command?type=create_human
            url_create = "http://127.0.0.1:8889/api/command?" + urllib.parse.urlencode({"type": "create_human"})
            req_create = urllib.request.urlopen(url_create)
            self.assertEqual(req_create.status, 200)
            data_create = json.loads(req_create.read().decode("utf-8"))

            # Kiểm tra số lượng con người tăng lên 4
            world_mod = next(m for m in data_create["modules"] if m["type"] == "world_state_summary")
            self.assertEqual(world_mod["data"]["humans_count"], 4)

            # 3. Test GET /api/command?type=disaster&val=Bao_Set
            url_disaster = "http://127.0.0.1:8889/api/command?" + urllib.parse.urlencode({"type": "disaster", "val": "Bao_Set"})
            req_disaster = urllib.request.urlopen(url_disaster)
            self.assertEqual(req_disaster.status, 200)
            data_disaster = json.loads(req_disaster.read().decode("utf-8"))

            world_mod_d = next(m for m in data_disaster["modules"] if m["type"] == "world_state_summary")
            self.assertEqual(world_mod_d["data"]["weather"], "Bao_Set")

            # 4. Test GET /api/auto_toggle
            req_toggle = urllib.request.urlopen("http://127.0.0.1:8889/api/auto_toggle")
            self.assertEqual(req_toggle.status, 200)
            data_toggle = json.loads(req_toggle.read().decode("utf-8"))
            self.assertTrue(data_toggle["auto_run"])

            # Tắt lại auto run
            urllib.request.urlopen("http://127.0.0.1:8889/api/auto_toggle")

        finally:
            server.shutdown()
            server.server_close()


if __name__ == "__main__":
    unittest.main()
