from fastapi.testclient import TestClient
import pytest
from app.main import app
from app.security import create_access_token


def pytest_configure():
    return {'last_created_tweet_id': 0}


@pytest.fixture
def client():
    yield TestClient(app)
    
    
@pytest.fixture
def test_user_1(client):
    user_data = {
        "username": "test_user_1",
        "email": "test1@mail.com",
        "phone_number": "004056787878",
        "password": "g&H)F36ma-lfpd.sda",
    },
    res = client.post("/users/", json=user_data)

    assert res.status_code == 201

    user_1 = res.json()
    user_1['password'] = user_data['password']
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