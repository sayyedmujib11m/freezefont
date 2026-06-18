from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {
        "app": "FreezeFont",
        "status": "running"
    }

@app.get("/hello")
def hello():
    return {
        "message": "FreezeFont API is working"
    }