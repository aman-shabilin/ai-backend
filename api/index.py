from dotenv import load_dotenv
from fastapi import FastAPI, Query
from routers.pinecone import VectorStore
from fastapi.middleware.cors import CORSMiddleware
from infra.models import ChatResponse, ChatRequest
from agents.agent import get_agent, ask_outlet_query, ask_product_query

load_dotenv()

app = FastAPI()

origins=[
    "https://localhost:8000",
    "https://v0-interactive-web-qblmwgpqahg.vercel.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

vector_store = VectorStore()

@app.on_event("startup")
async def initialize_vector_store():
    if vector_store.is_vector_store_empty("zusdrinkware", "default"):
        print("Vector store is empty. Scraping and loading documents...")
        raw = vector_store.scrape()
        docs = vector_store.split_product(raw)
        vector_store.add_documents(docs)
        print("Vector store initialized with new documents.")
    else:
        print("Vector store already contains vectors. Skipping re-indexing.")

@app.post("/chat", response_model = ChatResponse)
async def chat(request: ChatRequest):

    result = get_agent().chat(request.prompt)
    # DEBUG: print conversation so far
    print("[Memory DEBUG]", get_agent().agent.memory.chat_memory.messages)
    return ChatResponse(response=result)

@app.get("/products", response_model = ChatResponse)
async def get_products(query: str = Query(..., description="Ask about ZUS drinkware")):
    results = ask_product_query(query)
    return ChatResponse(response=results)

@app.get("/outlets", response_model= ChatResponse)
async def get_outlets(query: str = Query(..., description="Ask about ZUS outlets")):
    results = ask_outlet_query(query)
    return ChatResponse(response=results)

@app.get("/")
async def root(): 
    return {"message": "API is running"}
