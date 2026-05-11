import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

def get_db():
    """Establish connection to MongoDB."""
    uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/sentryx")
    client = MongoClient(uri)
    # Return the 'sentryx' database
    return client.get_database()