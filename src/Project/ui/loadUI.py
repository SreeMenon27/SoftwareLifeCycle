import streamlit as st
from src.Project.utils.config import Config

class LoadStreamlitUI:
    def __init__(self):
        self.config = Config()
        self.user_controls = {}

    def initialize_session(self):
        """Initialize Streamlit session state"""
        if "workflow_options" not in st.session_state:
            st.session_state["workflow_options"] = {}

        if "sdlc_progress" not in st.session_state:
            st.session_state["sdlc_progress"] = {
                "requirements": "",
                "user_stories": "",
                "po_feedback": "",
                "design_documents": "",
                "design_review_feedback": "",
                "generated_code": "",
                "code_review_feedback": "",
                "security_review_feedback": "",
                "test_cases": "",
                "test_review_feedback": "",
                "qa_feedback": "",
                "deployment_status": "",
                "monitoring_updates": "",
                "final_decision": None,
            }

        if "GROQ_API_KEY" not in st.session_state:
            st.session_state["GROQ_API_KEY"] = ""

    def loadStreamlit(self):
        """Load the Streamlit UI"""
      
        st.set_page_config(page_title=self.config.get_page_title(), layout="wide")
        self.initialize_session()  # ✅ Ensure session is initialized

        # Custom CSS for styling
        st.markdown("""
        <style>
            .main-header {
                font-size: 2.5rem;
                color: #1E3A8A;
                font-weight: 800;
                margin-bottom: 1rem;
                text-align: center;
            }
            .sub-header {
                font-size: 1.2rem;
                color: #4B5563;
                font-style: italic;
                margin-bottom: 2rem;
                text-align: center;
            }
            .sub-header1 {
                font-size: 1.2rem;
                color: #4B5563;
                margin-bottom: 2rem;
                text-align: left;
            }
            .footer {
                text-align: center;
                margin-top: 2rem;
                color: #6B7280;
                font-size: 0.8rem;
            }
            .section-divider {
                margin: 2rem 0;
                border-top: 1px solid #E5E7EB;
            }
            .btn-primary {
                background-color: #1E40AF;
                color: white;
                font-weight: 600;
                padding: 0.5rem 1rem;
                border-radius: 0.3rem;
                border: none;
                transition: background-color 0.3s;
            }
            .btn-primary:hover {
                background-color: #1E3A8A;
            }
        </style>
        """, unsafe_allow_html=True)

        # --- UI Header ---
        st.title("🚀 AI-Powered Software Development Lifecycle")
        st.write("Define your software development workflow with AI automation.")
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

        with st.sidebar:
            # --- User Inputs ---            

            self.user_controls["llm_choice"] = st.selectbox("🤖 Choose an LLM:", options=self.config.get_llm_options())

            if self.user_controls['llm_choice'] == "Groq":
                # Model selection
                self.user_controls["model_choice"] = st.selectbox("🤖 Choose a Model:",options=self.config.get_groq_model_options())

                # API key
                self.user_controls["GROQ_API_KEY"] = st.session_state["GROQ_API_KEY"] = st.text_input("🔑 Enter your API key:",type="password")

                if not self.user_controls["GROQ_API_KEY"]:
                    st.warning("Please enter the GROQ API KEY to proceed.")


            # ✅ Only store API key if entered (prevents overwriting with empty value)
            if self.user_controls["GROQ_API_KEY"]:
                st.session_state["GROQ_API_KEY"] = self.user_controls["GROQ_API_KEY"]


        use_case = st.text_input("🔍 Enter your use case:", placeholder="E.g., AI-driven SDLC automation")

        # -- Conditional Nodes ---
       
        st.markdown('<div class="sub-header1">⚡ Additional Workflow Options</div>', unsafe_allow_html=True)
        self.user_controls["enable_security_review"] = st.checkbox("Include Security Review")
        self.user_controls["enable_human_review"] = st.checkbox("Require Human Approval for Critical Steps")


        # --- Submit Button ---
        if st.button("🚀 Generate Workflow", type="primary"):
            # 🔥 Validation: Ensure API Key is entered before proceeding
            if not st.session_state.get("GROQ_API_KEY"):
                st.warning("⚠️ Please enter your API key to proceed.")
                return  # 🚨 Stop execution if API key is missing

            if not use_case:
                st.error("⚠️ Please enter a valid use case before proceeding!")
                return  # Stop execution if no use case is provided

            st.success(f"✅ Generating workflow for: **{use_case}** using LLM: **{self.user_controls['llm_choice']}**")

            # 🚀 Workflow options dictionary
            workflow_options = {
                "use_case": use_case,
                "llm_choice": self.user_controls["llm_choice"],
                "model_choice": self.user_controls["model_choice"],
                "GROQ_API_KEY": st.session_state["GROQ_API_KEY"],
                "security_review": self.user_controls["enable_security_review"],
                "human_approval": self.user_controls["enable_human_review"]
            }

            # ✅ Store options in session state
            st.session_state["workflow_options"] = workflow_options  

            # 🔍 Debugging: Show selected options
            st.write("### 🔍 Selected Workflow Options")
            st.json(workflow_options)

            # ✅ Confirm that the workflow is saved
            st.write("✅ Workflow input saved! Next, we'll generate the SDLC graph.")

            # 🛠 Debugging: Print session state only in development
            if __name__ == "__main__":
                print("Session State Initialized:", st.session_state)

        # Footer
        st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)
        st.markdown('<div class="footer">AI-Powered Software Development Lifecycle © 2025 | Powered by LangChain and Groq</div>', unsafe_allow_html=True)