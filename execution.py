
import ast
import re


def extract_code(text):
    match = re.search(
        r"```(?:python)?\s*(.*?)```",
        text,
        re.DOTALL | re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    return text.strip()


def validate_python_code(code):
    try:
        ast.parse(code)
        return True, "Python syntax validation passed."

    except SyntaxError as error:
        message = (
            f"Syntax error on line {error.lineno}: {error.msg}"
        )
        return False, message
