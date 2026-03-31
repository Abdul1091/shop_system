import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.main import app
from app.database import Base, get_db
from app.core.security import create_access_token

# 1. Setup an In-Memory SQLite Database for tests
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def session():
    # Create tables
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Drop tables after each test to ensure isolation
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(session):
    # Override the get_db dependency
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    # Clear overrides after test
    app.dependency_overrides.clear()

@pytest.fixture
def auth_headers():
    """Helper to generate a token for an owner user"""
    def _headers(user_id: int, role: str = "owner"):
        token = create_access_token({"sub": str(user_id), "role": role})
        return {"Authorization": f"Bearer {token}"}
    return _headers