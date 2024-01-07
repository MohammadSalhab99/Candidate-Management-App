from pydantic import BaseModel, Field,validator

import uuid

class User(BaseModel):
    first_name: str
    last_name: str
    email: str
    password:str
    uuid: str =str(uuid.uuid4())
    