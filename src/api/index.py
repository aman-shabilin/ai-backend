import os
from fastapi import FastAPI
from dotenv import load_dotenv
from ..prompt.prompt import SYSTEM_PROMPT
from fastapi.middleware.cors import CORSMiddleware
from ..infra.models import ChatResponse, ChatRequest
from ..agents.llm import ChatGemini

app = FastAPI()
def get_model():
    load_dotenv()

    gemini_api_key = os.getenv("GOOGLE_API_KEY")

    if not gemini_api_key:
        ValueError("GOOGLE_API_KEY environment variable is not set")

    model = ChatGemini(api_key=gemini_api_key, system_prompt=SYSTEM_PROMPT)
    return model

origins=[
    "https://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
)

@app.post("/chat", response_model = ChatResponse)
async def chat(request: ChatRequest):

    result = get_model().chat(request.prompt)
    return ChatResponse(response=result)
        
@app.get("/")
async def root(): 
    return {"message": "API is running"}
