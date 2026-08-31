from fastapi import FastAPI
# run with uvicorn app:app --reload
app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello, World!"}