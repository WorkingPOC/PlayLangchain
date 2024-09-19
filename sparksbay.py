import os
from dotenv import find_dotenv, load_dotenv

from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_google_genai import ChatGoogleGenerativeAI
from langserve import add_routes
from fastapi import FastAPI

def startserver():
    if __name__ =="__main__":
        import uvicorn
        uvicorn.run(app, host="localhost", port=8000)


 # 1. Create templates 
system_template = "CAR specifications"
prompt_template= ChatPromptTemplate.from_messages ([
    ('system', system_template),
    ('user','{car_name}')
])

# 2. connect AI
load_dotenv(find_dotenv())
os.getenv('GOOGLE_API_KEY')

model = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temparature=0.8,
    max_tokens=None,
    timeout=None,
    max_retries= 2,
)

#3. create parser
parser = StrOutputParser()

#4.create chain
chain = prompt_template | model | parser

# 5. App definition
app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)

# 6. Addin chain route
add_routes(
    app,
    chain,
    path="/chain",
)
startserver()

