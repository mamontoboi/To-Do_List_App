import configparser
from fastapi import FastAPI
from pymongo import MongoClient

from routes import router

config = configparser.ConfigParser()
config.read('../config.ini')

database_url = config['DEFAULT']['DB_URL']
database_name = config['DEFAULT']['DB_NAME']
# secret_key = config['DEFAULT']['SECRET_KEY']

app = FastAPI(debug=True)


@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(database_url)
    app.database = app.mongodb_client[database_name]
    print("Connected to DB!")


@app.on_event("shutdown")
def shutdown_db_client():
    print("Disconnected from DB")
    app.mongodb_client.close()


app.include_router(router, tags=["tasks"], prefix="/task")

