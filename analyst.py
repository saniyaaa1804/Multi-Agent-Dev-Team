
from langchain_ollama import ChatOllama
from utils.prompts import ANALYST_PROMPT


def analyst_agent(state):
    llm = ChatOllama(
        model="qwen2.5:3b",
        temperature=0.2
    )

    response = llm.invoke([
        ("system", ANALYST_PROMPT),
        ("human", state["user_requirement"])
    ])

    log = state.get("execution_log", [])
    log.append("Analyst Agent: Requirement analysis completed.")

    return {
        "analysis": response.content,
        "execution_log": log
    }
