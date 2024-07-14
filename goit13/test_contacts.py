import pytest
from fastapi.testclient import TestClient
from main import app
from dependencies.database import get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models.user import Base as UserBase
from models.contact import Base as ContactBase

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:pass@localhost:5432/goit11"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="module")
def client():
    UserBase.metadata.create_all(bind=engine)
    ContactBase.metadata.create_all(bind=engine)
    def override_get_db():
        try:
            db = TestingSessionLocal()
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    UserBase.metadata.drop_all(bind=engine)
    ContactBase.metadata.drop_all(bind=engine)

def test_create_contact(client):
    user_data = {"email": "user@example.com", "password": "password"}
    user_response = client.post("/api/v1/users/", json=user_data)
    assert user_response.status_code == 200
    login_response = client.post("/api/v1/users/login", data={"username": "user@example.com", "password": "password"})
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    contact_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john@example.com",
        "phone_number": "1234567890",
        "birthday": "1990-01-01",
        "additional_info": "Friend"
    }
    response = client.post("/api/v1/contacts/", json=contact_data, headers=headers)
    assert response.status_code == 200
    assert response.json()["first_name"] == "John"
