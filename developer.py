
from langchain_ollama import ChatOllama
from utils.prompts import DEVELOPER_PROMPT
from utils.execution import extract_code


def developer_agent(state):
    llm = ChatOllama(
        model="qwen2.5:3b",
        temperature=0.1
    )

    prompt = DEVELOPER_PROMPT.format(
        requirement=state.get("user_requirement", ""),
        analysis=state.get("analysis", ""),
        test_feedback=state.get("test_result", "No previous test feedback."),
        review_feedback=state.get("review_result", "No previous review feedback.")
    )

    response = llm.invoke(prompt)
    response_text = response.content

    generated_code = extract_code(response_text)

    attempt = state.get("retry_count", 0) + 1

    log = state.get("execution_log", [])
    log.append(
        f"Developer Agent: Code generated (attempt {attempt})."
    )

    return {
        "generated_code": generated_code,
        "execution_log": log
    }
