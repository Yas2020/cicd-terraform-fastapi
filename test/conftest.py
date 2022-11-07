from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.models import Base
from app.oauth2 import create_access_token
from app import models

# This module contains all the fixtures and is automatically available to all testing modules in the test package.

# We need a new database instance for our testing environment called fastapi_test
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)

@pytest.fixture
def test_user2(client):
    user_data = {"email": "hello1234@example.com",
                 "password": "E12345"
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user(client):
    user_data = {"email": "hello123@example.com",
                 "password": "E1234"
    }
    res = client.post("/users/", json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def token(test_user):
    return  create_access_token({"user_id": test_user['id']})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {**client.headers, "authorization": f"Bearer {token}"}
    return client


@pytest.fixture 
def test_posts(test_user, test_user2, session):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id'],},{
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']    
        },{
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
        },{
        "title": "4rd title",
        "content": "4rd content",
        "owner_id": test_user2['id']
        }]
    posts = list(map(lambda x: models.Post(**x), posts_data))
    session.add_all(posts)
    session.commit()
    return session.query(models.Post).all()