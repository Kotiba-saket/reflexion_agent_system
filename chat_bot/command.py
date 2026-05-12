
from typing import _TypedDict, Annotated
import operator
from langchain.messages import HumanMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langgraph.graph import END, StateGraph, add_messages
from langgraph.types import Command
load_dotenv()

class state(_TypedDict): 
    text: Annotated[str, operator.concat]

def node_a(state:state):
    print("NODE A")
    return Command(
        goto="node_b",
        update={
            "text": "a"
        }
    ) 

def node_b(state:state):
    print("NODE B")
    return Command(
        goto="node_c",
        update={
            "text": "b"
        }
    ) 
 
 
def node_c(state:state):
    print("NODE C")
    return Command(
        goto=END,
        update={
            "text":  "c"
        }
    ) 
graph = StateGraph(state)
graph.add_node("node_a", node_a)
graph.add_node("node_b", node_b)
graph.add_node("node_c", node_c)
graph.set_entry_point('node_a')
app = graph.compile()
res = app.invoke({
    "text":""
})
print(res)

 
