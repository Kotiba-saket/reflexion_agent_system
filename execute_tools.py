import json
from typing import List
from langchain_core.messages import AIMessage, BaseMessage, ToolMessage
from langchain_community.tools import TavilySearchResults
from dotenv import load_dotenv

load_dotenv()
# create tavily search results tool message
tavily_tool = TavilySearchResults(max_results=5)

# function to execute search queries from answerquestion tool call
def execute_tools(state: List[BaseMessage]) -> List[BaseMessage]:
     if not state:
          return []

     last_ai_message = state[-1]
     if not isinstance(last_ai_message, AIMessage):
          return []

     #Extract tool calls from the last AI message

     if not hasattr(last_ai_message, "tool_calls") or not last_ai_message.tool_calls:
          return []
     
     # process each tool call and execute it
     tool_messages = []

     for tool_call in last_ai_message.tool_calls:
          call_id = tool_call["id"]
          tool_name = tool_call.get("name")

          if tool_name == "AnswerQuestion":
               tool_args = tool_call.get("args", {}).get("search_queries", [])

               # execute each search query using the tavily tool
               query_results = {}
               for query in tool_args:
                    search_result = tavily_tool.run(query)
                    query_results[query] = search_result

               tool_messages.append(
                    ToolMessage(
                         content=json.dumps(query_results),
                         tool_call_id=call_id,
                    )
               )
          else:
               # Acknowledge non-search tool calls so every tool_call_id is answered.
               tool_messages.append(
                    ToolMessage(content=json.dumps({"ok": True}), tool_call_id=call_id)
               )
     return tool_messages