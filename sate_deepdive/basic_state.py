from typing import TypedDict
from langgraph.graph import END, StateGraph


class SimpleState(TypedDict):
    count: int

def increment(state: SimpleState) -> SimpleState:
    return {"count": state["count"] + 1}

def event_loop(state: SimpleState) -> str:
    if state["count"] >= 5:
        return "stop"
    return "continue"


graph = StateGraph(SimpleState)
graph.add_node("increment", increment)
graph.add_conditional_edges(
    "increment",
    event_loop,
    {
        "continue": "increment",
        "stop": END,  
    })
graph.set_entry_point("increment")
app = graph.compile()
state =  {"count": 0}
response = app.invoke(state)
print(response)
 

 