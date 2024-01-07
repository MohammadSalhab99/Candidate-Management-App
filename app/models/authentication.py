from pydantic import BaseModel


class authentication_request(BaseModel):
    email :str
    password:str
    


class authentication_response(BaseModel):
        token:str