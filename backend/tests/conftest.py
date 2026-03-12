import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.core.database import Base, get_db
from app.main import app
from app.models.user import User, UserRole

TEST_DATABASE_URL = "sqlite://"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session():
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    yield session
    session.close()
    transaction.rollback()
    connection.close()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


def register_verify_login(client, email: str, password: str = "password123"):
    reg = client.post(
        "/api/v1/auth/register", json={"email": email, "password": password}
    )
    assert reg.status_code == 200, reg.text

    verification_token = reg.json().get("verification_token")
    if verification_token:
        verify = client.get(f"/api/v1/auth/verify-email?token={verification_token}")
        assert verify.status_code == 200, verify.text

    login = client.post(
        "/api/v1/auth/login", data={"username": email, "password": password}
    )
    assert login.status_code == 200, login.text
    access = login.json()["access_token"]
    return {"Authorization": f"Bearer {access}"}


@pytest.fixture()
def user_headers(client):
    return register_verify_login(client, "user@example.com")


@pytest.fixture()
def admin_headers(client, db_session):
    res = client.post(
        "/api/v1/auth/register",
        json={"email": "admin@gmail.com", "password": "admin1234"},
    )
    assert res.status_code == 200, res.text

    admin = db_session.query(User).filter(User.email == "admin@gmail.com").first()
    admin.role = UserRole.admin
    db_session.commit()

    login_resp = client.post(
        "/api/v1/auth/login",
        data={"username": "admin@gmail.com", "password": "admin1234"},
    )
    assert login_resp.status_code == 200, login_resp.text
    token = login_resp.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}
