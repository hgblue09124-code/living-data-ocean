def state_transition_manager(current_state: str, action: str, allowed_transitions: dict) -> dict:
    state_rules = allowed_transitions.get(current_state, {})
    if action in state_rules:
        next_state = state_rules[action]
        return {
            "next_state": next_state,
            "allowed": True,
            "reason": None
        }
    return {
        "next_state": current_state,
        "allowed": False,
        "reason": f"Action '{action}' is not allowed from state '{current_state}'"
    }
