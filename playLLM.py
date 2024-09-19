

import os
from dotenv import find_dotenv, load_dotenv
from fastapi import FastAPI
from langchain_google_genai import ChatGoogleGenerativeAI, HarmCategory,HarmBlockThreshold
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langserve import add_routes
#init env
load_dotenv(find_dotenv())
os.getenv("GOOGLE_API_KEY")

llm = ChatGoogleGenerativeAI(
    model = "gemini-1.5-pro",
    temperature= 0,
    max_output_tokens= None,
    max_retries= 2,
    timeout= None,    
)

system_template = "translate from englist to {input}"
prompt_template= ChatPromptTemplate.from_messages ([
    ('system', system_template),
    ('user','{text}')
])

parser = StrOutputParser()

chain =prompt_template | llm | parser 

app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)
add_routes(app, chain, path="/chain")


if __name__ =="__main__":
        import uvicorn
        uvicorn.run(app, host="localhost", port=8000)
        
