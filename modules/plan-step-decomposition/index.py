def plan_step_decomposition(goal: str, subtasks: list = None) -> dict:
    if not subtasks:
        subtasks = [f"Execute goal: {goal}"]

    plan_steps = []
    for idx, task in enumerate(subtasks, start=1):
        plan_steps.append({
            "step_id": idx,
            "title": task,
            "status": "pending"
        })

    return {
        "goal": goal,
        "plan_steps": plan_steps
    }
