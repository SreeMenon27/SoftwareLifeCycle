import os
import streamlit as st
from langchain_groq import ChatGroq

class GroqLLM:
    def __init__(self,workflow_options):
        self.workflow_options = workflow_options

    def get_llm_model(self):
        try:
            groq_api_key = self.workflow_options["GROQ_API_KEY"]
            selected_model = self.workflow_options["model_choice"]
            if groq_api_key == '' and os.environ['GROQ_API_KEY'] == '':
                st.error("Please enter the API Key")

            llm = ChatGroq(api_key=groq_api_key, model=selected_model)

        except Exception as e:
            raise ValueError(f"Error occured with Exception : {e}")
        
        return llm
                
