
from state import AgentState
from agents.manager import manager_agent
from agents.analyst import analyst_agent
from agents.developer import developer_agent
from agents.tester import tester_agent
from agents.reviewer import reviewer_agent


def run_multi_agent(requirement, simulate_failure=False):
    """
    Custom Python coordinator.
    Runs five specialized agents without LangGraph.
    """

    state: AgentState = {
        "user_requirement": requirement,
        "retry_count": 0,
        "simulate_failure": simulate_failure,
        "failure_injected": False,
        "execution_log": []
    }

    def run_agent(agent_function):
        result = agent_function(state)

        # Update shared state with the agent's response.
        state.update(result)

    # Stage 1: Initial planning and analysis
    run_agent(manager_agent)
    run_agent(analyst_agent)

    # Stage 2: Development, testing and review loop
    max_retries = 2

    while True:
        run_agent(developer_agent)
        run_agent(tester_agent)
        run_agent(reviewer_agent)

        if state.get("review_status") == "APPROVE":
            break

        if state.get("retry_count", 0) >= max_retries:
            break

    # Stage 3: Final coordination
    if state.get("review_status") == "APPROVE":
        final_output = (
            "The development team successfully reviewed and approved "
            "the generated solution."
        )
    else:
        final_output = (
            "The workflow ended after reaching the maximum revision limit. "
            "Manual review is required."
        )

    state["final_output"] = final_output
    state["execution_log"].append(
        "Coordinator: Multi-agent workflow completed."
    )

    return state
