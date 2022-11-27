from app import schemas
import pytest
from jose import jwt
from app.config import settings


def test_root(client):
    res = client.get("/")
    # print(res.json().get('message'))
    # assert res.json().get('message') == 'Hello World; Files are synced with Docker'
    assert isinstance(res.json().get('message'), str)
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/", json={'email': 'hello123@example.com',
    'password': 'E1234'})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == 'hello123@example.com'
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user["email"], "password":test_user["password"]})
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == int(test_user['id'])
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

## We want to test a combination of wrong inputs here, so we use this decorator
@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'E1234', 403),
    ('hello123', 'wrongpasswrod', 403),
    ('wrong@example.com', 'wrongpassword', 403),
    (None, 'E1234', 422),
    ('Hellow1234', None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data={"username": email, "password": password})
    assert res.status_code == status_code
