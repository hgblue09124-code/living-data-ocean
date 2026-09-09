"""
Mô-đun Atomic xử lý tác động Action của External Agent (ActionResolverModule).
"""

from typing import Optional, Callable, List, Dict, Any, Tuple
from underworld.interface.observation import Observation
from underworld.interface.action import Action


class ActionResolverModule:
    """
    Trách nhiệm: Nhận Observation, gọi callback của External Agent và chuyển đổi danh sách Action sang dict payload cho World.tick().
    """

    def resolve_agent_actions(
        self,
        observation: Observation,
        agent_callback: Optional[Callable[[Observation], Optional[List[Action]]]] = None
    ) -> Tuple[Optional[List[Action]], Optional[List[Dict[str, Any]]]]:
        """
        Gọi agent_callback và trả về tuple (external_actions, actions_payload).
        """
        if agent_callback is None:
            return None, None

        external_actions = agent_callback(observation)
        if not external_actions:
            return None, None

        actions_payload = [act.to_dict() for act in external_actions]
        return external_actions, actions_payload
