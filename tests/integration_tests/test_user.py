from models.user_models import User_Auth, User_Details


def test_create_user(test_client):
    body = {
        "username": "tom@email.com",
        "password": "Password1",
        "first_name": "Tom",
        "last_name": "Smith"
    }

    response = test_client.post("/user/create_user", json=body)
    assert response.status_code == 200
    data = response.json()
    assert "user_id" in data
    assert "username" in data
    assert "password" not in data
    assert "first_name" in data
    assert "last_name" in data


def test_create_existing_user(test_client):
    body = {
        "username": "tom1@email.com",
        "password": "Password1",
        "first_name": "Tom",
        "last_name": "Smith"
    }

    response = test_client.post("/user/create_user", json=body)
    response2 = test_client.post("/user/create_user", json=body)
    assert response2.status_code == 400
    data = response2.json()
    assert data["detail"] == "Username already exists"


def test_create_user_required_fields(test_client):
    body = {

        "password": "Password1",
        "first_name": "Tom",
        "last_name": "Smith"
    }
    response = test_client.post("/user/create_user", json=body)
    assert response.status_code == 422
    body = {

        "username": "tom2@email.com",
        "first_name": "Tom",
        "last_name": "Smith"
    }
    response2 = test_client.post("/user/create_user", json=body)
    assert response2.status_code == 422


def test_create_user_optional_fields(test_client):
    body = {
        "username": "tom3@email.com",
        "password": "Password1"

    }
    response = test_client.post("/user/create_user", json=body)
    assert response.status_code == 200

    data = response.json()
    assert "user_id" in data
    assert data["username"] == "tom3@email.com"
    assert "password" not in data
    assert data["first_name"] is None
    assert data["last_name"] is None


def test_login_success(test_client, db_session, create_user_fixture):
    user = create_user_fixture
    assert user["user_id"]
    body = {
        "username": "tom4@gmail.com",
        "password": 'Password1'

    }

    response = test_client.post("user/token", data=body)
    data = response.json()
    assert "access_token" in data


def test_incorrect_username_password(test_client):
    pass
