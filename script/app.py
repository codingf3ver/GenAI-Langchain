import streamlit as st
from langgraph.checkpoint.memory import InMemorySaver
from langchain_tavily import TavilySearch
from dotenv import load_dotenv
import os
from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langchain.chat_models import init_chat_model

# Load environment variables
load_dotenv()
TAVILY_API_KEY = os.environ.get('TAVILY_API_KEY')

# Initialize memory for LangGraph
memory = InMemorySaver()

# Define state
class State(TypedDict):
    messages: Annotated[list, add_messages]

def chatbot(state: State):
    return {"messages": [llm.invoke(state["messages"])]}


# The first argument is the unique node name
# The second argument is the function or object that will be called whenever
# the node is used.


# Create the LangGraph state graph
graph_builder = StateGraph(State)

# Initialize LLM (Bedrock - Claude)
llm = init_chat_model(
    "anthropic.claude-3-5-sonnet-20240620-v1:0",
    model_provider="bedrock_converse",
)

# Initialize Tavily tool

# tool = TavilySearch(max_results=2,TAVILY_API_KEY)
# tools = [tool]

# Compile graph
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)
graph = graph_builder.compile(checkpointer=memory)

# Streamlit UI
st.title("LangGraph + Tavily Search Chatbot")

# Chat input
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
if prompt := st.chat_input("Say something..."):
    st.session_state.messages.append({"role": "user", "content": prompt})

    config = {"configurable": {"thread_id": "1"}}

    # Stream events from LangGraph
    events = graph.stream(
        {"messages": [{"role": "user", "content": prompt}]},
        config,
        stream_mode="values",
    )

    # Display AI responses in real-time
    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""
        for event in events:
            last_message = event["messages"][-1].content
            full_response = last_message
            response_container.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})
