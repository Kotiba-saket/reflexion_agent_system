from typing import Annotated, List, TypedDict
from langgraph.graph import END, StateGraph
import operator

class SimpleState(TypedDict):
    count: int
    sum: Annotated[int,operator.add]
    history: Annotated[List[int], operator.concat]

def increment(state: SimpleState) -> SimpleState:
    new_count = state["count"] + 1
    return {
            "count": new_count, 
            "sum": new_count,
            "history": [new_count]
            }

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
state =  {"count": 0, "sum": 0, "history": []}
response = app.invoke(state)
print(response)
 

 