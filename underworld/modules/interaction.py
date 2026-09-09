"""
Mô-đun Atomic quản lý quy tắc tương tác giữa các thực thể trong không gian (InteractionRule).
"""

from typing import List, Dict, Any
from underworld.modules.event import EventLog


class InteractionRule:
    """
    Sở hữu quy tắc phát hiện và xử lý tương tác giữa các thực thể trong không gian.
    """

    def process_interactions(
        self,
        humans_list: list,
        time_step: int,
        event_log: EventLog
    ) -> List[Dict[str, Any]]:
        """
        Phát hiện tương tác giữa các Human dựa trên khoảng cách Manhattan <= 1.
        """
        interaction_events = []
        for i in range(len(humans_list)):
            for j in range(i + 1, len(humans_list)):
                h1, h2 = humans_list[i], humans_list[j]
                dist = h1.spatial.manhattan_distance(h2.spatial.position)
                if dist <= 1:
                    event_dict = {
                        "time_step": time_step,
                        "type": "TUONG_TAC_HUMAN",
                        "human_1": h1.identity.id,
                        "human_2": h2.identity.id,
                        "chi_tiết": f"Human {h1.identity.id} và Human {h2.identity.id} gặp gỡ tại {h1.spatial.position}"
                    }
                    event_log.record_processed_event(event_dict)
                    interaction_events.append(event_dict)

                    # Cập nhật nhu cầu xã hội và trạng thái
                    h1.needs.needs["xã_hội"] = min(100.0, h1.needs.needs["xã_hội"] + 10.0)
                    h2.needs.needs["xã_hội"] = min(100.0, h2.needs.needs["xã_hội"] + 10.0)
                    h1.needs.status = "gặp_gỡ"
                    h2.needs.status = "gặp_gỡ"

        return interaction_events
