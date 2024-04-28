from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def heath_check_handler():
    return {"ping": "pong"}
