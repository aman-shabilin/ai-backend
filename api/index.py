import os
from fastapi import FastAPI, Query
from dotenv import load_dotenv
from routers.pinecone import VectorStore
from fastapi.middleware.cors import CORSMiddleware
from infra.models import ChatResponse, ChatRequest
from agents.llm import ChatGemini

app = FastAPI()

def get_model():
    load_dotenv()

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

vector_store = VectorStore()

@app.post("/chat", response_model = ChatResponse)
async def chat(request: ChatRequest):

    result = get_model().chat(request.prompt)
    return ChatResponse(response=result)

@app.get("/products")
def get_products(query: str = Query(..., description="Search product"), response_model = ChatResponse):

    raw_text = vector_store.scrape()
    documents = vector_store.split_product(raw_text)
    vector_store.add_documents(documents)

    results = vector_store.similarity_search("tumbler", k=5)
    return [r.page_content for r in results]

@app.get("/")
async def root(): 
    return {"message": "API is running"}
