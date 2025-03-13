# graph.py
from langgraph.graph import StateGraph
from pydantic import BaseModel
from typing import List, Dict, Any
from langchain_core.messages import SystemMessage, HumanMessage
from langchain.output_parsers import PydanticOutputParser

# Import your existing State class
from src.Project.workflow.state import State

class UserStory(BaseModel):
    id: str
    title: str
    description: str
    acceptance_criteria: List[str]

class Requirements_Output(BaseModel):
    title: str
    functional_requirements: List[str]
    non_functional_requirements: List[str]
    constraints: List[str]
    user_stories: List[UserStory]

def generate_requirements(llm, use_case: str):
    parser = PydanticOutputParser(pydantic_object=Requirements_Output)
    prompt = (
        f"You are an AI assistant specializing in software development lifecycle (SDLC) methodologies. Your role is to analyze, structure, and generate well-defined software requirements, user stories, and specifications based on given use cases. Ensure that responses follow best industry practices, adhere to clear formatting, and maintain logical consistency. Use markdown formatting."
        f"Generate detailed software requirements for the use case: '{use_case}'.\n"
        f"Output format: {parser.get_format_instructions()}"
    )
    response = llm.invoke(prompt)
    print("Response from LLM:", response)  # Debugging
    print("Response content:", response.content)  # Debugging
    return parser.parse(response.content)

class SDLCGraph:
    def __init__(self, llm, workflow_options):
        self.graph = StateGraph(State)  # Use State class as the state schema
        self.llm = llm
        self.workflow_options = workflow_options

        self.graph.add_node("generate_requirements", self.handle_requirements)
        self.graph.set_entry_point("generate_requirements")
        self.graph.set_finish_point("generate_requirements")

    def handle_requirements(self, state):
        print("State before processing:", state)
        print("Type of state before processing:", type(state))

        # Ensure state is an instance of State
        if not isinstance(state, State):
            state = State(**state)  # Convert dictionary to State object

        print("State before processing:", state)  # Debugging
        use_case = self.workflow_options["use_case"]
        requirements_output = generate_requirements(self.llm, use_case)

        if requirements_output:
            state.messages.append({
                "role": "assistant",
                "content": requirements_output.model_dump_json()
            })
        else:
            state.messages.append({
                "role": "assistant",
                "content": "Failed to generate requirements."
            })

        print("State after processing:", state)  # Debugging
        print("Type of state after processing:", type(state))
        
        return state

    def get_graph(self):
        return self.graph.compile()