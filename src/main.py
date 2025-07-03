from fastapi import FastAPI
from .agents.agent import parser, get_response
from .prompt.prompt import SYSTEM_PROMPT, format_prompt
from fastapi.middleware.cors import CORSMiddleware
from .infra.models import ChatResponse, ChatRequest
from .agents.llm import ChatGemini, gemini_api_key
from langchain.prompts import PromptTemplate

app = FastAPI()

prompt_template = PromptTemplate.from_template(SYSTEM_PROMPT)

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

    response = model.chat(prompt_template.format(request=request.prompt,format_instructions=parser.get_format_instructions()))
    parsed_response = parser.parse(response.content)

    return get_response(parsed_response)

        
@app.get("/")
async def root(): 
    return {"message": "API is running"}
