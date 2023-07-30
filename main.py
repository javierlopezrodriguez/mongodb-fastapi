from fastapi import FastAPI
from dotenv import dotenv_values
from pymongo import MongoClient
from routes import router as flower_router
import logging

config = dotenv_values(".env")
# converts the .env file contents into a dictionary

app = FastAPI()
# Set the logging level to DEBUG for the FastAPI application
# Set up the logging configuration
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)

# Event handler to connect to the Atlas MongoDB cluster on startup
@app.on_event("startup")
def startup_db_client():
    app.mongodb_client = MongoClient(config["ATLAS_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to the MongoDB database!")

# Event handler to close the connection on shutdown
@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()

# Root / endpoint that returns a welcome message
@app.get("/")
async def root():
    return {"message": "MongoDB Root Endpoint"}


# Registering /flower endpoints for the API
app.include_router(flower_router, tags=["flowers"], prefix="/flower")