from fastapi import FastAPI
from contextlib import asynccontextmanager
from database import pool, get_connection, init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    pool.open()
    # use psql fantasy_marketplace in terminal to connect to database, \dt to see tables, \d <table_name> to see table schema
    init_db()
    try:
        yield
    finally:
        pool.close()
        print("Shutting down...")

# run with uvicorn app:app --reload
app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {"message": "Hello, World!"}