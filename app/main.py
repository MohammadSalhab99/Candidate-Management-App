from fastapi import FastAPI, Depends, HTTPException, status, Query
from fastapi.middleware.cors import CORSMiddleware
from app.database import MongoDB
from app.services.user_service import UserService, Token
from app.services.candidate_service import CandidateService
from app.models.user import User
from app.models.candidate import Candidate
from app.models.authentication import authentication_request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from dotenv import load_dotenv
import os
from datetime import timedelta
from app.utils.json_encoder import CustomJSONEncoder
import json

# Load environment variables from .env file
load_dotenv()

# Initialize FastAPI app
app = FastAPI()
app.json_encoder = CustomJSONEncoder

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB Configuration
mongo_db = MongoDB()
mongo_db.connect()

# Default route
@app.get("/")
async def root():
    return {"message": "Hello World"}

# Health check route
@app.get("/health", status_code=200)
async def health_check():
    raise HTTPException(status_code=200, detail="200")

# User Service
user_service = UserService(mongo_db)

# Candidate Service
candidate_service = CandidateService(mongo_db)

# Dependency for User Authentication
def get_current_user(token: str = Depends(user_service.get_current_user)):
    return token

# Routes for User

# Create user route
@app.post("/user", response_model=dict)
def create_user(user: User):
    """Create a new user."""
    user_service.create_user(user)
    return {"message": "User created successfully"}

# User authentication route
@app.post("/login", response_model=object)
def authenticate_user(auth_request: authentication_request):
    """Authenticate user and return access token."""
    return user_service.authenticate_user(auth_request.email, auth_request.password)

# Token route to generate access token
@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    """Generate access token for a valid user."""
    user = user_service.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = user_service.create_access_token(
        data={"sub": user['email']}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Get all users route
@app.get("/users")
def get_users():
    """Get a list of all users."""
    return user_service.get_users()

# Routes for Candidates

# Create candidate route
@app.post("/candidate")
def create_candidate(candidate: Candidate, current_user: User = Depends(get_current_user)):
    """Create a new candidate."""
    id,uuid = candidate_service.create_candidate(candidate)
    return {"message": "Candidate created successfully", "candidate_id": str(id),"uuid":uuid}

# Get candidate by UUID route
@app.get("/candidate/{candidate_uuid}")
def get_candidate(candidate_uuid: str, current_user: User = Depends(get_current_user)):
    """Get candidate details by UUID."""
    return candidate_service.get_candidate_by_uuid(candidate_uuid)

# Update candidate by UUID route
@app.put("/candidate/{candidate_uuid}")
def update_candidate(candidate_uuid: str, candidate: Candidate, current_user: User = Depends(get_current_user)):
    """Update candidate details by UUID."""
    str(candidate_service.update_candidate(candidate_uuid, candidate))
    return {"message":"Candidate updated successfully"}

# Delete candidate by UUID route
@app.delete("/candidate/{candidate_uuid}")
def delete_candidate(candidate_uuid: str, current_user: User = Depends(get_current_user)):
    """Delete candidate by UUID."""
    candidate_service.delete_candidate(candidate_uuid)
    return {"message":"Candidate deleted successfully"}
    
# Get all candidates route
@app.get("/all_candidates")
def get_all_candidates(current_user: User = Depends(get_current_user)):
    """Get a list of all candidates."""
    return candidate_service.get_all_candidates()

# Search candidates for a specific user by a dynamic attribute
@app.get("/all_candidates/search", response_model=list)
def search_candidates(attribute: str = Query(...), value: str = Query(...),
                      current_user: User = Depends(user_service.get_current_user)):
    """Search candidates based on a dynamic attribute."""
    candidates = candidate_service.search_candidates(attribute, value)

    # Manually convert ObjectId to string for serialization
    serialized_candidates = json.loads(json.dumps(candidates, cls=CustomJSONEncoder))

    return serialized_candidates

# Run the FastAPI app using uvicorn
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
