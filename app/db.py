from pymongo import MongoClient
from app.config import MONGO_URI

class MongoDB:
    """
    A class to handle interactions with a MongoDB database.
    Ensures that the MongoClient is created only when needed.
    """

    def __init__(self, uri=MONGO_URI):
        """
        Initializes the MongoDB configuration.

        Args:
            uri (str): The URI for the MongoDB server (default is from the config file).
        """
        self.uri = uri

    def _get_client(self):
        """
        Creates a new MongoClient instance.

        Returns:
            MongoClient: A new MongoDB client instance.
        """
        return MongoClient(self.uri)

    def insert_message(self, data):
        """
        Inserts a message document into the 'message' collection.

        Args:
            data (dict): A dictionary representing the message to be inserted into the collection.

        This method creates a new client, inserts the document, and closes the connection.
        """
        with self._get_client() as client:
            db = client.user_messages_db
            collection = db.message
            result = collection.insert_one(data)
            print(f'Inserted document ID: {result.inserted_id}')