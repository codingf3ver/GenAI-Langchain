from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langserve import add_routes
import uvicorn
import os
from langchain_community.llms.ollama import Ollama
from dotenv import load_dotenv

load_dotenv()
os.environ["OPENAI_API_KEY"]=os.getenv("OPENAI_API_KEY")

app=FastAPI(
    title='Lanchain server',
    version="1.0",
    description="a kanchain application"
)

add_routes(
    app,
    ChatOpenAI(),
    path="/openai"

)
model=ChatOpenAI()
llm=Ollama(model="llama3.2")

prompt1=ChatPromptTemplate.from_template("Write me an essay about {topic} with 100 words")
prompt2=ChatPromptTemplate.from_template("Write me an poem about {topic} with 100 words")

add_routes(
    app,
    model|prompt1,
    path="/essay"
)
add_routes(
    app,
    llm|prompt2,
    path="/poem"
)

if __name__=='__main__':
    uvicorn.run(app,host="localhost",port=8000)