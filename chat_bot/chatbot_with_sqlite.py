
from typing import _TypedDict, Annotated
from langchain.messages import HumanMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langgraph.graph import END, StateGraph, add_messages
from langgraph.checkpoint.sqlite import sqlite3,SqliteSaver
import uuid
 
load_dotenv()
sqlite_conn = sqlite3.connect("checkpoint.sqlite", check_same_thread=False)
memory = SqliteSaver(sqlite_conn)
config = {"configurable": {"thread_id": str(uuid.uuid4)}}
class BasicChatState(_TypedDict): 
    messages: Annotated[list, add_messages]
 
llm = ChatGroq(model="llama-3.1-8b-instant")
 
def chatbot(state: BasicChatState):
    return {
        "messages": [llm.invoke(state["messages"])]
    }
 
 
graph = StateGraph(BasicChatState)
graph.add_node("chatbot", chatbot)
graph.add_edge("chatbot", END)
graph.set_entry_point("chatbot")

app = graph.compile(checkpointer=memory)

while True:
    user_input = input("User :")
    if(user_input in ["exit", "end"]):
        break
    else:
        result = app.invoke({
            "messages": [HumanMessage(content= user_input)]
        },config=config)
        print(f"AI: {result["messages"][-1].content}")      # your state dict (messages, etc.)
 
# print(result)
# print("*" * 50)
# print(result2)
    