# tests/test_main.py

from fastapi.testclient import TestClient
from .main import app
from fastapi import status
from datetime import timedelta

import pytest

client = TestClient(app)
access_token =None
# Test health check endpoint
def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"detail": "200"}

# Test create user endpoint
def test_create_user():
    user_data = {
        "first_name": "test_first",
        "last_name":"last_first",
        "email": "test@example.com",
        "password": "testpassword",
    }
    response = client.post("/user", json=user_data)
    assert response.status_code == 200
    assert response.json() == {"message": "User created successfully"}

# Test login endpoint
# def test_login():
#     login_data = {"email": "test@example.com", "password": "testpassword"}
#     response = client.post("/login", json=login_data)
#     assert response.status_code == 200
#     assert "access_token" in response.json()
def test_login_for_access_token():
    # Assuming you have a test user with known credentials for authentication
    test_user_data = {
        "username": "test@example.com",
        "password": "testpassword",
    }

    # Send a POST request to /token with valid user credentials
    response = client.post(
        "/token",
        data={"username": test_user_data["username"], "password": test_user_data["password"]},
    )

    # Check if the response status code is 200
    assert response.status_code == status.HTTP_200_OK

    # Check if the response contains the necessary fields
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    # Optionally, you can decode the JWT token and check its contents
    # decoded_token = decode_token(response.json()["access_token"])
    # assert decoded_token["sub"] == test_user_data["username"]
    global access_token
    access_token = response.json()['access_token']

# Test create candidate endpoint
def test_create_candidate():
    candidate_data = {
            "first_name":"Sami",
            "last_name":"Salhab",
            "email":"sami@test.com",
            "career_level":"Mid Level",
            "job_major":"Computer Science",
            "years_of_experience":2,
            "degree_type":"Bachelor",
            "skills":["python","fastapi","mongodb"],
            "nationality":"Jordanian",
            "city":"Amman",
            "salary":"1000",
            "gender":"Male"
    }
    response = client.post("/candidate", json=candidate_data, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert "candidate_id" in response.json()

# Test get candidate by UUID endpoint
def test_get_candidate():
    candidate_id = "824f687c-f71e-4d03-8985-432a45d51a1d"  # Replace with a valid UUID
    response = client.get(f"/candidate/{candidate_id}", headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert "first_name" in response.json()  # Assuming "name" is a field in your Candidate model

# Test update candidate by UUID endpoint
def test_update_candidate():
    candidate_id = "824f687c-f71e-4d03-8985-432a45d51a1d"  # Replace with a valid UUID
    updated_data = {
    "first_name":"Khaled",
    "last_name":"salhab",
    "email":"Khaled@test.com",
    "career_level":"Mid Level",
    "job_major":"Computer Science",
    "years_of_experience":2,
    "degree_type":"Bachelor",
    "skills":["python","fastapi","mongodb"],
    "nationality":"Jordanian",
    "city":"Amman",
    "salary":"1000",
    "gender":"Male"
} 
    response = client.put(f"/candidate/{candidate_id}", json=updated_data, headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Candidate updated successfully"

# Test delete candidate by UUID endpoint
def test_delete_candidate():
    candidate_id = "824f687c-f71e-4d03-8985-432a45d51a1d"  # Replace with a valid UUID
    response = client.delete(f"/candidate/{candidate_id}",headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert response.json()["message"] == "Candidate deleted successfully"

# Test get all candidates endpoint
def test_get_all_candidates():
    response = client.get("/all_candidates",headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test search candidates endpoint
def test_search_candidates():
    search_params = {"attribute": "first_name", "value": "John Doe"}
    response = client.get("/all_candidates/search", params=search_params,headers={"Authorization": f"Bearer {access_token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Add more tests for other endpoints as needed
