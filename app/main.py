from fastapi import FastAPI
from mangum import Mangum

app = FastAPI()

@app.get("/")
def home():
    return {"message": "working"}

@app.get("/health")
def health():
    return {"status": "ok"}

handler = Mangum(app)