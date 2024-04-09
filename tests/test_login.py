from fastapi.testclient import TestClient
import main

def test_login_valid_credentials():
  """
  This test checks if the login endpoint returns a 200 status code
  for valid username and password credentials. It also checks a JWT token 
  is returned when successful.
  """

  with TestClient(main.app) as client:
    # Define valid username and password
    user = "test_user"
    password = "1234"

    # Prepare login data (can be a dictionary or JSON)
    data = {"username": user, "password": password}

    # Send a POST request to the login endpoint
    response = client.post("/user/login", json=data)

    # Assert the response status code
    assert response.status_code == 200, "Login failed with valid credentials"

    # Assert the response content (e.g., presence of a token)
    response_data = response.json()
    assert "access_token" in response_data
