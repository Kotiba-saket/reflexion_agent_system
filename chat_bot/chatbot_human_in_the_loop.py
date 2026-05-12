
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
class state(_TypedDict): 
    messages: Annotated[list, add_messages]

llm = ChatGroq(model="llama-3.1-8b-instant")

GENERATE_POST = "generate_post"
GET_REVIEW_DICISION = "get_review_decision"
POST = "post"
COLLECT_FEEDBACK = "collect_feedback" 

def generate_post(state: state):
    return {
        "messages": [llm.invoke(state["messages"])]
    }

def collect_review_decision(state:state):
    post_content = state["messages"][-1].content

    print(f"\n\n Current linkenIn post: \n {post_content} \n")

    dicision = input("Post to LinkedIn? (yes/no)")
    if(dicision.lower() =="yes"):
        return POST
    else: 
        return COLLECT_FEEDBACK
    
def post(state: state):
    final_post = state["messages"][-1].content
    print(f"\n\n Current linkenIn post approved: \n {final_post} \n")

def collect_feedback(state: state):
    feedback = input("How can i improve this post?")
    return {
        "messages": [HumanMessage(content=feedback)]
    }    

graph = StateGraph(state)
graph.add_node(GENERATE_POST,generate_post )
graph.add_node(GET_REVIEW_DICISION,collect_review_decision )
graph.add_node(COLLECT_FEEDBACK,collect_feedback )
graph.add_node(POST,post )

graph.set_entry_point(GENERATE_POST)

graph.add_conditional_edges(GENERATE_POST, collect_review_decision)
graph.add_edge(POST, END)
graph.add_edge(COLLECT_FEEDBACK, GENERATE_POST)

app = graph.compile()

response = app.invoke({
    "messages": [HumanMessage(content="Write me a LinkedIn post on AI Agents taking over content creation")]
})
print(response)