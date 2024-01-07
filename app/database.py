from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

class MongoDB:
    def __init__(self):
        """Initializes the MongoDB class."""
        self.client = None
        self.db = None

    def connect(self):
        """
        Connects to the MongoDB database using the provided environment variables.

        Environment Variables:
            MONGO_DB_URL (str): MongoDB connection URL.
            MONGO_DB_NAME (str): MongoDB database name.
        """
        db_url = os.getenv("MONGO_DB_URL")
        db_name = os.getenv("MONGO_DB_NAME")
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]

    def disconnect(self):
        """Disconnects from the MongoDB database."""
        if self.client:
            self.client.close()