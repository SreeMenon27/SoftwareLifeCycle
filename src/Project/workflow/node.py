from src.Project.workflow.state import State

class Node:
    def __init__(self, llm):
        self.llm = llm

    def invokeLLM(self, state:State)-> dict:
        return {"messages":self.llm.invoke(state["messages"])}