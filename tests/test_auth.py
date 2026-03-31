def test_register_user(client):
    response = client.post(
        "/auth/register",
        json={
            "name": "Abdullahi",
            "email": "test@example.com",
            "password": "password123",
            "role": "owner"
        }
    )
    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"

def test_login_success(client):
    # Register first
    client.post("/auth/register", json={
        "name": "Abdullahi", "email": "test@example.com", 
        "password": "password123", "role": "owner"
    })
    
    # Login via form data (OAuth2PasswordRequestForm)
    response = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()