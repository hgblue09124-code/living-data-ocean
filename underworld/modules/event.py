"""
Mô-đun Atomic quản lý vòng đời sự kiện mô phỏng (EventLog).
"""

import copy
from typing import List, Dict, Any, Optional


class EventLog:
    """
    Quản lý danh sách sự kiện và bảo tồn vòng đời sự kiện trước/trong/sau tick.
    """

    def __init__(self):
        """Khởi tạo nhật ký sự kiện."""
        self.events: List[Dict[str, Any]] = []

    def add_event(self, detail: str, event_type: str = "SU_KIEN_QUAN_TRI", time_step: Optional[int] = None) -> None:
        """Thêm một sự kiện mới vào danh sách."""
        evt = {
            "type": event_type,
            "chi_tiết": detail,
            "processed": False
        }
        if time_step is not None:
            evt["time_step"] = time_step
            evt["processed"] = True
        self.events.append(evt)

    def prepare_step_events(self, current_step: int) -> List[Dict[str, Any]]:
        """
        Chuẩn bị danh sách sự kiện cho bước hiện tại.
        Bảo tồn các sự kiện chưa được xử lý (ví dụ: tạo từ Administrator trước tick)
        và làm sạch danh sách sự kiện bước cũ.
        """
        pending_events = [e for e in self.events if not e.get("processed", False)]
        self.events = []

        for evt in pending_events:
            evt["time_step"] = current_step
            evt["processed"] = True
            self.events.append(evt)

        return self.events

    def record_processed_event(self, event_dict: Dict[str, Any]) -> None:
        """Ghi nhận trực tiếp một sự kiện đã xử lý trong tick."""
        event_dict["processed"] = True
        self.events.append(event_dict)

    def to_list(self) -> List[Dict[str, Any]]:
        """Xuất danh sách sự kiện dạng copy độc lập."""
        return copy.deepcopy(self.events)
