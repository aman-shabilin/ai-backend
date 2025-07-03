from fastapi import FastAPI
from .prompt.prompt import SYSTEM_PROMPT
from fastapi.middleware.cors import CORSMiddleware
from .infra.models import ChatResponse, ChatRequest
from .agents.llm import ChatGemini, gemini_api_key
from langchain.prompts import PromptTemplate

app = FastAPI()

model = ChatGemini(api_key=gemini_api_key, system_prompt=SYSTEM_PROMPT)

origins=[
    "https://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
)

@app.post("/chat", response_model = ChatResponse)
async def chat(request: ChatRequest):

    result = model.chat(request.prompt)
    print(f"Request : {request}")
    return ChatResponse(response=result)
        
@app.get("/")
async def root(): 
    return {"message": "API is running"}
