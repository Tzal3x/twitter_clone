from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.security import create_access_token


def create_header(username):
    token = create_access_token({'sub': username})
    return {"Authorization": "Bearer %s" % token}   


@pytest.fixture
def client():
    yield TestClient(app)
    
    
@pytest.fixture
def test_user_1(client):
    user_data = {
        "username": "test_user_1st",
        "email": "test1st@mail.com",
        "phone_number": "004056787899",
        "password": "g&H)F36ma-lfpd.sd."
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201

    user_1 = res.json()
    user_1['password'] = user_data['password']
    pytest.test_user_1_username = user_1['username']
    return user_1


@pytest.fixture
def token(test_user_1):
    return create_access_token({"user_id": test_user_1['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }

    return client