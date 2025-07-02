import os 
from fastapi import FastAPI
from .agents.agent import parser
from .prompt.prompt import SYSTEM_PROMPT
from fastapi.middleware.cors import CORSMiddleware
from .infra.models import ChatResponse, ChatRequest
from .agents.llm import ChatGemini, gemini_api_key, prompt_template

app = FastAPI()

origins=[
    "https://localhost:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
)

model = ChatGemini(api_key=gemini_api_key, system_prompt=SYSTEM_PROMPT)
@app.post("/chat", response_model = ChatResponse)
async def chat(request: ChatRequest):
    formatted_prompt = prompt_template.format(
        request = request.prompt,
        format_instructions = parser.get_format_instructions()
    )
    response = model.chat(prompt=formatted_prompt)

    parsed_response = parser.parse(response.content)
    print(f"Current response: {parsed_response}")
    if parsed_response.action=="use.tool" and parsed_response.tool_input:
        try:
            result = eval(parsed_response.tool_input, {"__builtins__": {}})
            return ChatResponse(response=str(result))
        except Exception:
            return ChatResponse(response="Invalid arithmetic expression.")
    else:
        return ChatResponse(response=parsed_response.response)

@app.get("/")
async def root(): 
    return {"message": "API is running"}
