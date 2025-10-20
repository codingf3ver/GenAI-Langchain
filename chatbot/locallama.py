from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_community.llms import ollama
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")

prompt_template=ChatPromptTemplate.from_messages(
    [
        ("system","you are a helpful assistant Please respond to then user queries"),
        ("user","Question:{question}")
    ]
)

st.title("lanchain demo with OLLAMA")
input_text = st.text_input("search the topic")

llm=ollama.Ollama(model="llama3.2")

output_parser = StrOutputParser()
chain=prompt_template|llm|output_parser

if input_text:
    st.write(chain.invoke({'question':input_text}))