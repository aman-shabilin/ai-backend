import os 
import uvicorn
from fastapi import FastAPI, Request
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

@app.get("/")
async def root(): 
    return {"message": "API is running"}
