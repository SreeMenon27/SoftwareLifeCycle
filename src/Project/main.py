import streamlit as st
from src.Project.utils.config import Config
from src.Project.ui.loadUI import LoadStreamlitUI
from src.Project.LLMs.llm import GroqLLM
from src.Project.workflow.graph import SDLCGraph, Requirements_Output
from src.Project.workflow.state import State

def load_main():
    ui = LoadStreamlitUI()
    ui.loadStreamlit()

    if "workflow_options" not in st.session_state or "use_case" not in st.session_state["workflow_options"]:
        st.warning("⚠️ Use case is not defined. Please go back and enter the details.")
        return

    try:
        llm_obj = GroqLLM(st.session_state["workflow_options"]).get_llm_model()
        
        if not llm_obj:
            st.error("❌ Error: LLM model cannot be initialized.")
            return
        
        usecase = st.session_state["workflow_options"]["use_case"]
        
        if not usecase.strip():
            st.error("❌ Error: No use case provided.")
            return

        st.write(f"🚀 Initializing SDLC workflow for: **{usecase}**")

        graph_obj = SDLCGraph(llm_obj, st.session_state["workflow_options"])
        sdlc_graph = graph_obj.get_graph()

        initial_state = State(messages=[])

        # Before invoking the graph
        print("Initial state before invoking graph:", initial_state)
        print("Type of initial state:", type(initial_state))

        result = sdlc_graph.invoke(initial_state)

        # After invoking the graph
        print("Result state after invoking graph:", result)
        print("Type of result state:", type(result))

        # Ensure result is an instance of State
        if not isinstance(result, State):
            print("Result is not an instance of State. Converting...")
            result = State(**result)  # Convert dictionary to State object

        print("Final result state:", result)
        print("Type of final result state:", type(result))

        if result and result.messages:
            last_message = result.messages[-1]["content"]
            try:
                structured_requirements = Requirements_Output.model_validate_json(last_message)
            except Exception as e:
                st.error(f"Error parsing requirements output: {e}")
                structured_requirements = None
        else:
            structured_requirements = None

        st.subheader("--- Generated user stories ---")

        if structured_requirements:
            st.write(f"**Title:** {structured_requirements.title}")
    
            with st.expander("Functional Requirements"):
                for req in structured_requirements.functional_requirements:
                    st.write(f"- {req}")

            with st.expander("Non-Functional Requirements"):
                for req in structured_requirements.non_functional_requirements:
                    st.write(f"- {req}")

            with st.expander("Constraints"):
                for constraint in structured_requirements.constraints:
                    st.write(f"- {constraint}")

            with st.expander("User Stories"):
                for story in structured_requirements.user_stories:
                    st.write(f"**ID:** {story.id}")
                    st.write(f"**Title:** {story.title}")
                    st.write(f"**Description:** {story.description}")
                    st.write(f"**Acceptance Criteria:**")
                    for criteria in story.acceptance_criteria:
                        st.write(f"- {criteria}")
                    st.write("---")
        else:
            st.write("No structured requirements generated.")

    except Exception as e:
        st.error(f"❌ Exception: {e}")
