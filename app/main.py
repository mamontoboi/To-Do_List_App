from fastapi import FastAPI
from pymongo import MongoClient
from .config import settings
from .routes import router

app = FastAPI()


@app.get("/api/test")
def test():
    return {"message": "The app is running smoothly."}


@app.get("/")
def root():
    return {"message": "Welcome to the app. Add '/docs' to your url to see the UI."}


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
