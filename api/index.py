import os
from fastapi import FastAPI, Query
from dotenv import load_dotenv
from routers.pinecone import VectorStore
from fastapi.middleware.cors import CORSMiddleware
from infra.models import ChatResponse, ChatRequest
from agents.llm import ChatGemini

app = FastAPI()

load_dotenv()

def get_model():

    gemini_api_key = os.getenv("GOOGLE_API_KEY")

    if not gemini_api_key:
        ValueError("GOOGLE_API_KEY environment variable is not set")

    model = ChatGemini(api_key=gemini_api_key)
    return model


origins=[
    "https://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
print("Pinecone API Key:", os.getenv("PINECONE_API_KEY"))
vector_store = VectorStore()

@app.on_event("startup")
async def initialize_vector_store():
    if vector_store.vector_store is None:
        print("Vector store is empty. Scraping and loading documents...")
        raw = vector_store.scrape()
        docs = vector_store.split_product(raw)
        vector_store.add_documents(docs)
        print("Vector store initialized.")
    else:
        print("Vector store already exists and is loaded.")

@app.post("/chat", response_model = ChatResponse)
async def chat(request: ChatRequest):

    result = get_model().chat(request.prompt)
    return ChatResponse(response=result)

@app.get("/products", response_model = ChatResponse)
async def get_products(query: str = Query(..., description="Search product")):

    vector_results = vector_store.similarity_search(query)

    results = get_model().chat(vector_results)
    print(f"Results: {vector_results}")
    return ChatResponse(response=results)

@app.get("/")
async def root(): 
    return {"message": "API is running"}
