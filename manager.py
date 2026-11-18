
from langchain_ollama import ChatOllama
from utils.prompts import MANAGER_PROMPT


def manager_agent(state):
    llm = ChatOllama(
        model="qwen2.5:3b",
        temperature=0.2
    )

    response = llm.invoke([
        ("system", MANAGER_PROMPT),
        ("human", state["user_requirement"])
    ])

    log = state.get("execution_log", [])
    log.append("Manager Agent: Task allocation completed.")

    return {
        "manager_plan": response.content,
        "execution_log": log
    }
