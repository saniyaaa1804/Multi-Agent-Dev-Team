
from typing import TypedDict, List


class AgentState(TypedDict, total=False):
    user_requirement: str
    manager_plan: str
    analysis: str
    generated_code: str
    test_result: str
    test_status: str
    requirements_check_status: str
    review_result: str
    review_status: str
    retry_count: int
    simulate_failure: bool
    failure_injected: bool
    execution_log: List[str]
    final_output: str
