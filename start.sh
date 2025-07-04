#!/bin/bash

# Run FastAPI (background)
uvicorn api.index:app --host 0.0.0.0 --port 8000 &

# Run Gradio (blocks)
python api/frontend.py