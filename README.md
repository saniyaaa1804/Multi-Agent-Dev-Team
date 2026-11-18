
# Multi-Agent Collaborative Development System

## Project Overview

An AI-powered multi-agent software development system built using Python, Streamlit, LangGraph and Ollama.

The application uses specialised agents to analyse requirements, generate code, test solutions and review the final output.

## Agents

1. Manager Agent - Coordinates the workflow.
2. Analyst Agent - Analyses software requirements.
3. Developer Agent - Generates Python code.
4. Tester Agent - Checks code and identifies issues.
5. Reviewer Agent - Approves or requests revisions.

## Features

- Role-based multi-agent architecture
- Shared workflow state
- Agent communication and hand-offs
- Testing and review workflow
- Feedback and revision loop
- Failure simulation
- Retry limit to prevent endless loops
- Execution trace
- Python code download

## Technology Stack

- Python
- Streamlit
- LangGraph
- LangChain
- Ollama
- Qwen 2.5 3B

## Installation

Create a virtual environment:

```bash
python -m venv venv
```

Activate on Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

Download the model:

```bash
ollama pull qwen2.5:3b
```

Run the application:

```bash
streamlit run app.py
```

## Workflow

User Requirement -> Manager -> Analyst -> Developer -> Tester -> Reviewer -> Final Output.

If the tester or reviewer identifies an issue, the workflow sends feedback to the Developer for revision, subject to a maximum retry limit.

## Author

Om Akolkar

B.Tech Computer Science and Engineering
AI and Analytics
MIT ADT University, Pune
