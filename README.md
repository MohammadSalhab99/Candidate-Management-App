# FastAPI Candidate Management App

This is a simple FastAPI application for managing candidate information. It includes CRUD operations for candidates and uses MongoDB as the database.

## Installation

1.  **Clone the repository:**

    ```bash
    git clone https://github.com/MohammadSalhab99/Candidate-Management-App.git

    ```

2.  **Create a .env file:**
    Create a .env file in the project root and add the following variables:

        MONGO_DB_URL=mongodb://mongo:27017/
        MONGO_DB_NAME=candidate_database
        SECRET_KEY=your_secret_key

Install dependencies:

## Usage

Using Docker Compose
Build and start the containers:

    docker-compose up --build
### Access the FastAPI app:

The app will be accessible at http://localhost:8000.

Access the API documentation:

Open http://localhost:8000/docs in your browser to interact with the Swagger UI for API documentation.

### Using Local Development
If you prefer to run the app locally without Docker Compose:

#### Run the FastAPI app:

    uvicorn main:app --host 0.0.0.0 --port 8000
    The app will be accessible at http://localhost:8000.

Access the API documentation:

Open http://localhost:8000/docs in your browser to interact with the Swagger UI for API documentation.

##  Endpoints
### Candidates
#### Create Candidate:

POST /candidate
#### Get Candidate by UUID:

    GET /candidate/{candidate_uuid}

#### Update Candidate by UUID:

    PUT /candidate/{candidate_uuid}
#### Delete Candidate by UUID:

    DELETE /candidate/{candidate_uuid}
#### Get All Candidates:

    GET /all_candidates

#### Search Candidates:

    GET /all_candidates/search?attribute={attribute}&value={value}
