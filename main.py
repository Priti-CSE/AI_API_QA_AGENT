from fastapi import FastAPI
app = FastAPI()
@app.get("/")
def home():
    return {"message": "AI API QA Agent is running"}