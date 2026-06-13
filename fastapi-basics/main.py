from fastapi import FastAPI
from pydantic import BaseModel

import ollama

app = FastAPI()

class ChatRequest(BaseModel):
    messages: str
    session_id: str

@app.get("/agent/status")
def get_status():
    return {"status": "running", "model": "qwen2.5:7b"}

@app.get("/agent/info")
def get_info():
    return {"name": "謝晨", "model": "qwen2.5:7b"}

@app.post("/agent/chat")
def post_chart(chartrequest: ChatRequest):
    
    respones = ollama.chat(model= "qwen2.5:7b",
                           messages=  [{"role": "user", "content": chartrequest.messages}]
    )

    return {"reply": respones["message"]["content"]} 