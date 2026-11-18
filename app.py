
import streamlit as st
from graph import run_multi_agent


st.set_page_config(
    page_title="Multi-Agent Development Team",
    layout="wide"
)

st.title("Multi-Agent Collaborative Development System")
st.caption("Unit IV: Multi-Agent Systems and Collaboration")

st.markdown(
    "A team of specialised AI agents collaborates to analyse "
    "requirements, generate code, test solutions and review results."
)

with st.sidebar:
    st.header("Agent Team")

    st.write("1. Manager Agent")
    st.write("2. Analyst Agent")
    st.write("3. Developer Agent")
    st.write("4. Tester Agent")
    st.write("5. Reviewer Agent")

    st.divider()

    simulate_failure = st.checkbox(
        "Simulate agent failure",
        help="Forces the first testing attempt to request revision."
    )

    st.caption("Maximum revision attempts: 2")


st.subheader("Software Requirement")

requirement = st.text_area(
    "Describe the application you want the agents to develop:",
    placeholder=(
        "Example: Create a Python program for a student "
        "grade calculator with input validation."
    ),
    height=130
)

if st.button("Start Agent Collaboration", type="primary"):

    if not requirement.strip():
        st.warning("Please enter a software requirement.")

    else:
        try:
            with st.spinner(
                "The multi-agent team is collaborating. Please wait..."
            ):
                result = run_multi_agent(
                    requirement,
                    simulate_failure
                )

            st.success("Agent workflow completed.")

            st.divider()
            st.subheader("Agent Execution Trace")

            for index, activity in enumerate(
                result.get("execution_log", []), 1
            ):
                st.write(f"{index}. {activity}")

            st.divider()
            st.subheader("Agent Outputs")

            with st.expander("Manager Agent - Task Allocation"):
                st.write(result.get("manager_plan", ""))

            with st.expander("Analyst Agent - Requirement Analysis"):
                st.write(result.get("analysis", ""))

            with st.expander("Developer Agent - Generated Code"):
                st.code(
                    result.get("generated_code", ""),
                    language="python"
                )

            with st.expander("Tester Agent - Testing Feedback"):
                st.write(result.get("test_result", ""))
                st.write(
                    "Testing Status:",
                    result.get("test_status", "Not available")
                )

            with st.expander("Reviewer Agent - Final Review"):
                st.write(result.get("review_result", ""))
                st.write(
                    "Review Status:",
                    result.get("review_status", "Not available")
                )

            st.divider()
            st.subheader("Final Workflow Result")
            st.write(result.get("final_output", ""))

            st.metric(
                "Revision Attempts",
                result.get("retry_count", 0)
            )

            st.download_button(
                "Download Generated Python Code",
                data=result.get("generated_code", ""),
                file_name="generated_solution.py",
                mime="text/x-python"
            )

        except Exception as error:
            st.error(f"Workflow error: {error}")
            st.exception(error)
