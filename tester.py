
import re
from langchain_ollama import ChatOllama
from utils.prompts import TESTER_PROMPT
from utils.execution import validate_python_code


def check_grade_calculator_requirements(code):
    """Check the important grade-calculator requirements."""

    issues = []

    # Check Python syntax separately.
    syntax_valid, syntax_message = validate_python_code(code)

    if not syntax_valid:
        return False, syntax_message

    # Check required functions.
    required_functions = [
        "get_valid_mark",
        "calculate_total_marks",
        "calculate_percentage",
        "assign_grade"
    ]

    for function in required_functions:
        if not re.search(
            rf"def\s+{function}\s*\(",
            code
        ):
            issues.append(
                f"Required function is missing: {function}"
            )

    # Check individual mark validation.
    if not re.search(
        r"0\s*<=\s*mark\s*<=\s*100",
        code
    ):
        issues.append(
            "Each subject mark must be validated between 0 and 100."
        )

    # Check repeated input until a valid mark is entered.
    if not re.search(
        r"def\s+get_valid_mark\s*\([^)]*\)\s*:"
        r"[\s\S]*?while\s+True",
        code
    ):
        issues.append(
            "get_valid_mark should repeatedly request input "
            "until a valid mark is entered."
        )

    # Check maximum possible marks.
    has_500 = bool(
        re.search(r"max_possible_marks\s*=\s*500\b", code)
        or re.search(r"/\s*500\b", code)
    )

    if not has_500:
        issues.append(
            "Percentage calculation must use 500 as the "
            "maximum possible marks."
        )

    # Reject an incorrect total limit of 100.
    if re.search(
        r"(?:total_marks|total)\s*>\s*100\b",
        code
    ):
        issues.append(
            "The program must not reject totals above 100. "
            "The valid maximum total is 500."
        )

    # Check grade assignment boundaries.
    grade_function = re.search(
        r"def\s+assign_grade\s*\([^)]*\)\s*:"
        r"([\s\S]*?)(?=\ndef\s+|\Z)",
        code
    )

    if grade_function:
        grade_code = grade_function.group(1)

        for boundary in [90, 80, 70, 60]:
            if not re.search(
                rf"\b{boundary}\b",
                grade_code
            ):
                issues.append(
                    f"Grade boundary {boundary} is missing."
                )
    else:
        issues.append("assign_grade function is missing.")

    if issues:
        return False, "\n".join(issues)

    return True, (
        "All grade calculator requirements passed: "
        "individual mark validation, five-subject total, "
        "percentage calculation and grade boundaries."
    )


def tester_agent(state):
    llm = ChatOllama(
        model="qwen2.5:3b",
        temperature=0.1
    )

    requirement = state.get("user_requirement", "")
    analysis = state.get("analysis", "")
    code = state.get("generated_code", "")

    # Run deterministic checks first.
    checks_passed, checks_feedback = (
        check_grade_calculator_requirements(code)
    )

    # Obtain an additional LLM review.
    prompt = TESTER_PROMPT.format(
        requirement=requirement,
        analysis=analysis,
        code=code,
        syntax_result=checks_feedback
    )

    response = llm.invoke(prompt)
    llm_feedback = response.content

    # Deterministic checks are authoritative.
    test_status = "PASS" if checks_passed else "REVISE"

    failure_injected = state.get("failure_injected", False)

    if state.get("simulate_failure", False) and not failure_injected:
        test_status = "REVISE"
        failure_injected = True

        checks_feedback += (
            "\nSIMULATED FAILURE: A controlled failure was "
            "injected for workflow demonstration."
        )

    combined_feedback = (
        f"DETERMINISTIC TEST RESULTS:\n{checks_feedback}\n\n"
        f"ADDITIONAL AI REVIEW:\n{llm_feedback}\n\n"
        f"FINAL TEST STATUS: {test_status}"
    )

    log = state.get("execution_log", [])
    log.append(
        f"Tester Agent: Testing completed. Status: {test_status}."
    )

    return {
        "test_result": combined_feedback,
        "test_status": test_status,
        "requirements_check_status": (
            "PASS" if checks_passed else "FAIL"
        ),
        "failure_injected": failure_injected,
        "execution_log": log
    }
