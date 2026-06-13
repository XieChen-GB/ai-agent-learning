from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    session_id: str

@app.get("/agent/status")
def get_status():
    return {"status": "running", "model": "qwen2.5:7b"}

@app.get("/agent/info")
def get_info():
    return {"name": "謝晨", "model": "qwen2.5:7b"}

@app.post("/agent/chat")
def post_char(chartrequest: ChatRequest):
    return {"reply": f"收到:{chartrequest.message}", "session": chartrequest.session_id} 