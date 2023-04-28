from fastapi import FastAPI
from pymongo import MongoClient
from .config import settings
from .routes import router

app = FastAPI()

# http://127.0.0.1:8000/api/login


@app.get("/favicon.ico")
async def favicon():
    return {"status": "ok"}


@app.get("/api/test")
def root():
    return {"message": "FastAPI is running."}


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(settings.DB_URL)
    app.database = app.mongodb_client[settings.DB_NAME]
    print("Connected to DB!")


@app.on_event("shutdown")
def shutdown_db_client():
    print("Disconnected from DB")
    app.mongodb_client.close()


app.include_router(router, tags=["tasks"], prefix="/api/tasks")
