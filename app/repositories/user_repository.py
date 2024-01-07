from app.database import MongoDB
from app.models.user import User
from bson.json_util import dumps


class UserRepository:
    def __init__(self, mongo_db: MongoDB):
        """Initializes the repository with a MongoDB instance."""
        self.collection = mongo_db.db["user"]

    def create_user(self, user_data: User) -> str:
        """Adds a new user to the database."""
        id = self.collection.insert_one(user_data.dict()).inserted_id
        return str(id)

    def get_user_by_uuid(self, uuid: str) -> dict:
        """Retrieves a user by UUID."""
        return self.collection.find_one({"uuid": uuid})

    def get_user_by_email(self, email: str) -> dict:
        """Retrieves a user by email address."""
        return self.collection.find_one({"email": email})

    def get_users(self) -> str:
        """Retrieves all users in JSON format."""
        all_users = self.collection.find()
        return dumps(all_users)
