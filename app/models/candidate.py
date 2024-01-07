from pydantic import BaseModel, Field
import uuid


class Candidate(BaseModel):
    first_name:str
    last_name:str
    email:str
    UUID: str =str(uuid.uuid4())
    career_level:str =Field(description="ex: Junior, Senior, Mid Level...")
    job_major:str = Field(description="ex: Computer Science, Computer Information Systems,...")
    years_of_experience:int
    degree_type:str = Field(description="ex: Bachelor, Master, High School,...")
    skills:list[str]
    nationality:str
    city:str
    salary:float
    gender:str = Field( default ="Not Specified",description = "[“Male”, “Female”, “Not Specified”]")
