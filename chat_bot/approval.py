
from typing import _TypedDict, Annotated
from langchain.messages import HumanMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langgraph.graph import END, StateGraph, add_messages
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import InMemorySaver 
from langgraph.types import Command
load_dotenv()
checkpointer = InMemorySaver()
config = {"configurable": {"thread_id": "1"}}

class BasicChatState(_TypedDict): 
    messages: Annotated[list, add_messages]

search_tool = TavilySearchResults(max_result =2)
tools =  [search_tool]
llm = ChatGroq(model="llama-3.1-8b-instant")
llm_with_tool = llm.bind_tools(tools=tools)

def model(state: BasicChatState):
    return {
        "messages": [llm_with_tool.invoke(state["messages"])]
    }

def tools_router(state: BasicChatState):
    last_message = state["messages"][-1]
    if(hasattr(last_message, "tool_calls") and len(last_message.tool_calls) > 0):
        return "tool_node"
    else: 
        return END
    
tool_node = ToolNode(tools=tools)

graph = StateGraph(BasicChatState)
graph.add_node("model", model)
graph.add_node("tool_node", tool_node)

graph.set_entry_point("model")
graph.add_conditional_edges("model", tools_router)
graph.add_edge("tool_node","model" )

app = graph.compile(checkpointer=checkpointer, interrupt_before=["tool_node"])
events = app.stream({
            "messages": [HumanMessage(content= "wat is de temperatuur in antwerpen?")]
        },config=config,stream_mode="values")
for event in events:
    event["messages"][-1].pretty_print()

events2 = app.stream(None,config=config,stream_mode="values")
for event in events2:
    event["messages"][-1].pretty_print()
    