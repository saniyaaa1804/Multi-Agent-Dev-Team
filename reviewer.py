
from langchain_ollama import ChatOllama
from utils.prompts import REVIEWER_PROMPT


def reviewer_agent(state):
    llm = ChatOllama(
        model="qwen2.5:3b",
        temperature=0.1
    )

    prompt = REVIEWER_PROMPT.format(
        requirement=state.get("user_requirement", ""),
        analysis=state.get("analysis", ""),
        code=state.get("generated_code", ""),
        test_status=state.get("test_status", "UNKNOWN"),
        test_feedback=state.get("test_result", "No tester feedback.")
    )

    response = llm.invoke(prompt)
    ai_review = response.content

    # Final approval is based on the Tester Agent's
    # deterministic checks, not an unsupported LLM objection.
    approved = (
        state.get("test_status") == "PASS"
        and state.get("requirements_check_status") == "PASS"
    )

    if approved:
        review_status = "APPROVE"
        review_feedback = (
            "STATUS: APPROVE\n\n"
            "The deterministic requirements checks passed. "
            "The solution satisfies the checked requirements. "
            "No additional features are required."
        )
    else:
        review_status = "REVISE"
        review_feedback = (
            "STATUS: REVISE\n\n"
            "The solution did not pass the Tester Agent's "
            "requirements checks.\n\n"
            + state.get("test_result", "")
        )

    retry_count = state.get("retry_count", 0)

    if not approved:
        retry_count += 1

    log = state.get("execution_log", [])
    log.append(
        f"Reviewer Agent: Review completed. Status: {review_status}."
    )

    return {
        "review_result": (
            review_feedback
            + "\n\nAdditional AI review:\n"
            + ai_review
        ),
        "review_status": review_status,
        "retry_count": retry_count,
        "execution_log": log
    }
