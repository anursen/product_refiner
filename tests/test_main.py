from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Product Refiner API"}

def test_refine_description():
    test_description = "Test description"
    response = client.post(
        "/refine/",
        json={"description": test_description}
    )
    assert response.status_code == 200
    assert "refined_description" in response.json()
    assert isinstance(response.json()["refined_description"], str)

def test_refine_description_invalid_input():
    response = client.post(
        "/refine/",
        json={}  # Missing required field
    )
    assert response.status_code == 422  # Validation error
