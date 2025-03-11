import streamlit as st
from src.Project.utils.config import Config
from src.Project.ui.loadUI import LoadStreamlitUI
from src.Project.LLMs.llm import ChatGroq


def load_main():
    """Starting point of the Software Lifecycle Project"""

    ui = LoadStreamlitUI()
    ui.loadStreamlit()

    if "workflow_options" not in st.session_state or "use_case" not in st.session_state["workflow_options"]:
        st.warning("⚠️ Use case is not defined. Please go back and enter the details.")
        return

    try:
        llm_obj = ChatGroq(api_key=st.session_state["workflow_options"]["GROQ_API_KEY"], model = st.session_state["workflow_options"]["model_choice "])
        
        if not llm_obj:
            st.error("❌ Error: LLM model cannot be initialized.")
            return
        
        # Initialize and set up the graph based on the use case
        usecase = st.session_state["workflow_options"]["use_case"]

        if not usecase.strip():  # Ensure use case isn't empty
            st.error("❌ Error: No use case provided.")
            return

        st.write(f"🚀 Initializing SDLC workflow for: **{usecase}**")

        # ✅ Placeholder for SDLC Graph Initialization
        # TODO: Add graph initialization logic here

    except Exception as e:
        st.error(f"❌ Exception: {e}")
