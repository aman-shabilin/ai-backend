from fastapi import FastAPI, Query
from agents.agent import get_agent, retrieve_tools
from routers.pinecone import VectorStore
from fastapi.middleware.cors import CORSMiddleware
from infra.models import ChatResponse, ChatRequest


app = FastAPI()

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
vector_store.describe()

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

    result = get_agent().chat(request.prompt)
    return ChatResponse(response=result)

@app.get("/products", response_model = ChatResponse)
async def get_products(query: str = Query(..., description="Ask about ZUS drinkware")):
    print("Vector store: {vector_store.vector_store}")
    results = retrieve_tools(query)
    return ChatResponse(response=results)

@app.get("/")
async def root(): 
    return {"message": "API is running"}
