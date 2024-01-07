from app.models.candidate import Candidate
from app.database import MongoDB
from app.repositories.candidate_repository import CandidateRepository
from fastapi import HTTPException, status
import uuid
import pandas as pd

class CandidateService:
    """
    Service class for managing candidate-related operations.
    Parameters:
        - mongo_db (MongoDB): An instance of the MongoDB class for database operations.
    """

    def __init__(self, mongo_db: MongoDB):
        """
        Initializes the CandidateService instance.
        Parameters:
            - mongo_db (MongoDB): An instance of the MongoDB class for database operations.
        """
        self.repository = CandidateRepository(mongo_db)

    def create_candidate(self, candidate_data: Candidate):
        """
        Creates a new candidate and inserts it into the database.
        Parameters:
            - candidate_data (Candidate): Candidate data to be inserted.

        Returns:
            - tuple: A tuple containing the inserted candidate's MongoDB ObjectId and UUID.
        """
        candidate = self.repository.get_candidate_by_email(candidate_data.email)
        if candidate:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Candidate Already Exists")

        candidate_uuid = str(uuid.uuid4())
        candidate_data.UUID = candidate_uuid
        inserted_id = self.repository.create_candidate(candidate_data)
        return inserted_id, candidate_uuid

    def get_candidate_by_uuid(self, uuid: str):
        """
        Retrieves a candidate by UUID from the database.
        Parameters:
            - uuid (str): The UUID of the candidate to retrieve.
        Returns:
            - Candidate: An instance of the Candidate model representing the retrieved candidate.
        Raises:
            - HTTPException: If the candidate with the specified UUID is not found.
        """
        candidate_data = self.repository.get_candidate_by_uuid(uuid)
        if not candidate_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")
        return Candidate(**candidate_data)

    def update_candidate(self, uuid: str, candidate: Candidate):
        """
        Updates a candidate in the database.
        Parameters:
            - uuid (str): The UUID of the candidate to update.
            - candidate (Candidate): Candidate data for the update.
        Returns:
            - dict: A dictionary containing information about the update.
        Raises:
            - HTTPException: If the candidate with the specified UUID is not found.
        """
        if not self.repository.get_candidate_by_uuid(uuid):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")
        return self.repository.update_candidate(uuid, candidate)

    def delete_candidate(self, uuid: str):
        """
        Deletes a candidate from the database.
        Parameters:
            - uuid (str): The UUID of the candidate to delete.
        Returns:
            - dict: A dictionary containing information about the deletion.
        Raises:
            - HTTPException: If the candidate with the specified UUID is not found.
        """
        if not self.repository.get_candidate_by_uuid(uuid):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Candidate not found")
        return self.repository.delete_candidate(uuid)

    def get_all_candidates(self):
        """
        Retrieves a list of all candidates from the database.

        Returns:
            - list: A list of dictionaries representing all candidates in the database.
        """
        return self.repository.get_all_candidates()

    def search_candidates(self, attribute: str, value: str):
        """
        Searches for candidates based on a specified attribute and value.

        Parameters:
            - attribute (str): The attribute to search for (e.g., "first_name").
            - value (str): The value to search for within the specified attribute.
        Returns:
            - list: A list of dictionaries representing candidates that match the search criteria.
        """
        return self.repository.search_candidates(attribute, value)
    
    def generate_csv_content(self):
        data = self.repository.get_all_candidates()
        df = pd.DataFrame(data)
        csv_content = df.to_csv(index=False).encode('utf-8')
        return csv_content