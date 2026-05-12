
from typing import _TypedDict, Annotated
from langchain.messages import HumanMessage
 
from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langgraph.graph import END, StateGraph, add_messages

load_dotenv()
llm = ChatGroq(model="llama-3.1-8b-instant")

class BasicChatState(_TypedDict): 
    messages: Annotated[list, add_messages]

def chatbot(state: BasicChatState):
    return {
        "messages": [llm.invoke(state["messages"])]
    }
graph = StateGraph(BasicChatState)

graph.add_node("chatbot", chatbot)
graph.set_entry_point("chatbot")
graph.add_edge("chatbot", END)


app = graph.compile()

while True:
    user_input = input("User :")
    if(user_input in ["exit", "end"]):
        break
    else:
        result = app.invoke({
            "messages": [HumanMessage(content= user_input)]
        })
    print(result["messages"][-1].content)
    print(result)

