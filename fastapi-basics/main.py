from fastapi import FastAPI
app = FastAPI()

@app.get("/agent/status")
def get_status():
    return {"status": "running", "model": "qwen2.5:7b"}

@app.get("/agent/info")
def get_info():
    return {"name": "謝晨", "model": "qwen2.5:7b"}