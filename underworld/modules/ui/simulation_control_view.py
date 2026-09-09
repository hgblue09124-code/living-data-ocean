"""UI Module chứa Bảng Điều khiển Mô phỏng (Simulation Control View)."""

from typing import Dict, Any, Optional, Callable
from underworld.modules.ui.base import UIModule


class SimulationControlViewModule(UIModule):
    """UI Module chuyên trách cung cấp các nút bấm điều khiển simulation mở rộng."""

    def __init__(self):
        super().__init__(
            module_id="ui_simulation_control_view",
            title="🎮 Bảng Điều Khiển Mô Phỏng (Simulation Control)",
            category="control"
        )

    def render_web_dict(self, world_state: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "module_id": self.module_id,
            "title": self.title,
            "category": self.category,
            "type": "control_panel",
            "data": {
                "actions": [
                    {"id": "step_1", "label": "⏭️ Step 1 Tick", "endpoint": "/api/step?n=1"},
                    {"id": "auto_2s", "label": "▶️ Bật/Tắt Auto 1s", "endpoint": "/api/auto_toggle"},
                    {"id": "add_human", "label": "➕ Thêm Con Người", "endpoint": "/api/command?type=create_human"},
                    {"id": "trigger_storm", "label": "⚡ Thiên Tai Bão", "endpoint": "/api/command?type=disaster&val=Bão Sét"},
                    {"id": "weather_rain", "label": "🌧️ Mưa lớn", "endpoint": "/api/command?type=weather&val=Mưa lớn"},
                    {"id": "weather_clear", "label": "☀️ Nắng đẹp", "endpoint": "/api/command?type=weather&val=Nắng đẹp"}
                ]
            }
        }
