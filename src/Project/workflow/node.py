from src.Project.workflow.state import State

class Node:
    def __init__(self, model):
        self.llm = model

    def invokeLLM(self, state:State)-> dict:
        return {"messages":self.llm.invoke(state["messages"])}