from app.models.candidate import Candidate
from app.database import MongoDB
from bson.json_util import dumps
import json
class CandidateRepository:
    def __init__(self, mongo_db: MongoDB):
        """Initializes the repository with a MongoDB instance."""
        self.collection = mongo_db.db["candidate"]

    def create_candidate(self, candidate: Candidate) -> str:
        """Adds a new candidate to the database."""
        return str(self.collection.insert_one(candidate.dict()).inserted_id)

    def get_candidate_by_uuid(self, uuid: str) -> dict:
        """Retrieves a candidate by UUID."""
        return self.collection.find_one({"UUID": uuid})

    def update_candidate(self, uuid: str, candidate: Candidate) -> dict:
        """Updates a candidate's information."""
        response = self.collection.replace_one({"UUID": uuid}, candidate.dict())
        return response

    def delete_candidate(self, uuid: str) -> dict:
        """Removes a candidate from the database."""
        return self.collection.delete_one({"UUID": uuid})

    def get_all_candidates(self) -> list:
        """Retrieves all candidates from the database."""
        response = self.collection.find()
        response = json.loads(dumps(response))
        return response

    def search_candidates(self, attribute: str, value: str) -> list:
        """Searches candidates by a specific attribute."""
        query = {attribute: {"$regex": value, "$options": "i"}}
        candidates_data = self.collection.find(query)
        return list(candidates_data)

    def get_candidate_by_email(self, email: str) -> dict:
        """Retrieves a candidate by email address."""
        return self.collection.find_one({"email": email})