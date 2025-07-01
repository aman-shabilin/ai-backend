import os 
from dotenv import load_dotenv
from .infra.models import ChatResponse, ChatRequest
from .agents.ai_agent import chat_chain
from langchain_core.messages import HumanMessage
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins=[
    "https://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
)

@app.post("/chat", response_model = ChatResponse)
async def chat(request: ChatRequest):
    response = chat_chain.predict(input=request.prompt)
    return ChatResponse(response=response.content)

@app.get("/")
async def root(): 
    return {"message": "API is running"}
